#!/usr/bin/env python
from codebrowser import CodeBrowser

from bottle import debug, route, run
from jinja2 import Environment, PackageLoader, Template
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter


# SETUP
class Animal(object):
    def speak(self, call):
        print call

class Baby(object):
    pass

class Cute(Baby):
    pass

class Cat(Animal, Cute):
    def speak(self):
        super(Cat, self).speak("meow")


# HELPER FUNCTIONS
def highlight_source(source):
    """
    Highlight some python source code with HTML formatting.
    """
    return highlight(source, PythonLexer(), HtmlFormatter())

def render_results(context, template_name="index.html"):
    """
    Template rendering boilerplate goes here.
    """
    env = Environment(loader=PackageLoader("codebrowser", "templates"))
    template = env.get_template(template_name)
    styles = HtmlFormatter().get_style_defs(".highlight")
    context["styles"] = styles
    return template.render(context)

def show_object_info(obj):
    highlighted_sources = []

    cb = CodeBrowser(obj)
    class_sources = cb.get_class_history()

    for source in class_sources:
        highlighted_sources.append( highlight_source(source) )

    context = {
        "obj_attrs": cb.get_attrs(),
        "class_sources": highlighted_sources,
    }

    page = render_results(context)
    return page


# URLS
@route("/")
def index():
    c = Cat()
    return show_object_info(c)

@route("/class_code/:class_code")
def class_code(class_code):
    return class_code


# START SERVER
debug(mode=True)
run(host="localhost", port=8080, reloader=True)

