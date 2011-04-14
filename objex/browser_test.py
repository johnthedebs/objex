#!/usr/bin/env python
from objex import Objex

import sys
import traceback

from bottle import debug, redirect, route, run
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

env = {
    "obj": Cat(),
    "trail": [],
}


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
    environment = Environment(loader=PackageLoader("objex", "templates"))
    template = environment.get_template(template_name)
    styles = HtmlFormatter().get_style_defs(".highlight")
    context["styles"] = styles
    return template.render(context)

def show_object_info(obj):
    cb = Objex(obj)
    highlighted_sources = []

    # Get highlighted class history
    class_sources = cb.get_class_history()
    for source in class_sources:
        highlighted_sources.append( highlight_source(source) )

    context = {
        "cb": cb,
        "class_sources": highlighted_sources,
        "object_source": cb.get_object_source(),
        "traceback": traceback.extract_stack(),
        "trail": env["trail"],
    }

    page = render_results(context)
    return page


def explore_object(obj):
    # URLS
    @route("/")
    def index():
        return show_object_info(env["obj"])

    @route("/attr/:attr")
    def class_code(attr):
        global env
        # Save current object
        env["trail"].append(env["obj"])
        # Set new object
        env["obj"] = getattr(env["obj"], attr)
        redirect("/")

    # START SERVER
    debug(mode=True)
    run(host="localhost", port=8080, reloader=True)

