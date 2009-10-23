"""
django-widgets template tags
"""

from django.template import Library, Node, TemplateSyntaxError
from django_widgets.loading import registry

register = Library()


def _parse_args(bits, parser):
    if len(bits) < 2:
        raise TemplateSyntaxError("'%s' takes at least one argument"
                                  " (registered widget name)" % bits[0])
    return (bits[1], parser.compile_filter(bits[2]) if len(bits)>2 else None)


def _parse_options(bits, parser):
    options = {}
    opts_arg = None
    if len(bits) > 3:
        bits = iter(bits[3:])
        for bit in bits:
            for arg in bit.split(","):
                if '=' in arg:
                    k, v = arg.split('=', 1)
                    k = k.strip()
                    options[k] = parser.compile_filter(v)
                elif arg:
                    opts_arg = parser.compile_filter(arg)
    return (options, opts_arg,)


class IncludeWidgetNode(Node):
    def __init__(self, widget_name, value, opts_arg, options):
    	self.widget_name = widget_name
        self.value = value
        self.options = options
        self.opts_arg = opts_arg

    def render(self, context):
        resolved_options = dict(zip(self.options.keys(), [self.options[v].resolve(context) for v in self.options]))
        if self.opts_arg:
            resolved_options.update(self.opts_arg.resolve(context))
        return registry.get(self.widget_name).render(context, 
                self.value.resolve(context) if self.value else None, 
                resolved_options)


class WidgetNode(Node):
    def __init__(self, widget_name, value, opts_arg, options, nodelist):
    	self.widget_name = widget_name
        self.value = value
        self.options = options
        self.opts_arg = opts_arg
        self.nodelist = nodelist

    def render(self, context):
        resolved_options = dict(zip(self.options.keys(), [self.options[v].resolve(context) for v in self.options]))
        if self.opts_arg:
            resolved_options.update(self.opts_arg.resolve(context))
        widget = registry.get(self.widget_name)
        ctx = widget.get_context( 
                self.value.resolve(context) if self.value else None, 
                resolved_options)
        context.update(ctx)
        output = self.nodelist.render(context)
        context.pop()
        return output


@register.tag(name='include_widget')
def include_widget(parser, token):
    bits = token.split_contents()
    name, value = _parse_args(bits, parser)
    options, opts_arg = _parse_options(bits, parser)
    return IncludeWidgetNode(name, value, opts_arg, options)


@register.tag(name='widget')
def widget(parser, token):
    bits = token.split_contents()
    name, value = _parse_args(bits, parser)
    options, opts_arg = _parse_options(bits, parser)
    nodelist = parser.parse(('endwidget',))
    parser.delete_first_token()
    return WidgetNode(name, value, opts_arg, options, nodelist)
