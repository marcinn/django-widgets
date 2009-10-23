"""
django widgets base module

author: Marcin Nowak
license: BSD
"""

from django.forms.widgets import MediaDefiningClass
from django.forms.widgets import Widget as BaseWidget
from django.template.loader import get_template
from loading import registry


class WidgetMeta(MediaDefiningClass):
    """
    initializes widget classes
    automatically adds widget instance into registry
    """

    def __init__(mcs, name, bases, attrs):
        MediaDefiningClass.__init__(mcs, name, bases, attrs)
        if 'template' not in attrs:
            mcs.template = None
        mcs.template_instance = None
        if name is not 'Widget':
            registry.register(name, mcs())


class Widget(BaseWidget):
    """
    base widget class
    """
    __metaclass__ = WidgetMeta
    template = None

    def __init__(self, *args, **kwargs):
        super(BaseWidget, self).__init__(*args, **kwargs)
        self.template_instance = None

    def get_context(self, value, options):
        """
        returns context dictionary
        output my be customized by options dict
        """
        return {}

    def render(self, context, value=None, attrs=None):
        """
        main render method
        uses "template" class property for rendering
        or needs to be overriden for custom non-template widgets
        """
        if not self.template_instance:
            if not self.template:
                raise RuntimeError('Abstract method Widget.render()\
                        is not implemented')
            self.template_instance = get_template(self.template)

        context.push()
        context.update(self.get_context(value, attrs or {}))
        result = self.template_instance.render(context)
        context.pop()
        return result
               
