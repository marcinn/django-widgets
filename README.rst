django-widgets
==============

An alternative for templatetags.  Based on http://code.google.com/p/django-widgets/

Background
----------

Django template tags are great, but writing renderes and compiler functions is
often boring (ie. parsing options). 

Common usage of widgets is similar to {% with %}..{% include %} pair, but
provides easy-to-use interface for more complex view-logic code.
Major features are: class-based style and widgets registry with autodiscovering.

Django-widgets provides two useful templatetags with option parsers:

- **include_widget**

    Simply includes widget instance found in registry by name, calls widget`s 
    render() method with provided optional value and configuration.
   
    Syntax:

        {% include_widget widget_name [value] [option1=value1, [option2=value2, ...]] %}

    value     - optional value passed as `value` in get_context() and render() methods
    opt1=val1 - dictionary key-value pairs passed as `options` in get_context() and render()


- **widget**
    
    Same as include_widget tag, but template source is taken from tag content
    instead of widget`s default template. 
    
    Everything within {% widget %} and {% endwidget %} is used as template source.
    Also this template tag does NOT call widget`s render() method, but only 
    get_context() instead.


Hints:

-   Context of your view will be unchanged.
-   Context of widget contains all view variables, similar to {% with %} tag.
    No more hacks like {{ settings.MEDIA_URL }} or {% get_media_url %} :)


Defining a Widget
-----------------

Widgets should extend from django_widgets.base.Widget class.
Every widget, placed in widgets.py module of your app,
is automatically registered by name (from class.__name__)

Simplest "hello world" widget example (place it in yourapp/widgets.py module):

    from django_widgets import Widget
    
    class HelloWorld(Widget):
        def render(self, context, value=None, options=None):
            return u'Hello world!'
    

Calling from template:

    {% load widgets %}
    
    <h1>{% include_widget HelloWorld %}</h1>


Base Widget class has render() method which uses class-property
**template** for rendering. But if not set render() raises
NotImplementedError.


Example of widget with custom template:


    from django_widgets import Widget
    from catalog import Category
    
    class CategoryTree(Widget):
        template = 'catalog/category_tree_widget.html'
    
        def get_context(self, root_category, options):
            return {
                'tree': Category.objects.get_tree_for(root_category),
                'root_category': root_category,
                'max_level': options.get('max_level', 3),
                }
    


In template:


    {% load widgets %}
    
    {% include_widget CategoryTree max_level=1 %}
    

The `catalog/category_tree_widget.html` template will be used for
rendering tree of categories. 


Or use inline tempalte with {% widget %} tag:


    {% load widgets %}
    
    {% widget CategoryTree max_level=1 %}
        <div>
            ... widget template ...
        </div>
    {% endwidget %}



