#!/usr/bin/env python
from objex import Objex

import os.path
import sys
import traceback

from bottle import debug, error, redirect, request, response, route, run, static_file
from jinja2 import Environment, PackageLoader, Template
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter


# SETUP
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

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
    "obj": None,
    "history": [],
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

    internal_attrs = []
    private_attrs = []
    attrs = []
    for attr in cb.get_attrs():
        if str(attr[0]).startswith("__"):
            internal_attrs.append(attr)
        elif str(attr[0]).startswith("_"):
            private_attrs.append(attr)
        else:
            attrs.append(attr)

    context = {
        "attrs": attrs,
        "cb": cb,
        "class_sources": highlighted_sources,
        "internal_attrs": internal_attrs,
        "private_attrs": private_attrs,
        "traceback": traceback.extract_stack(),
        "trail": env["trail"],
    }

    page = render_results(context)
    return page

# URLS
@route("/")
def index():
    if not env["obj"]:
        env["obj"] = request
    return show_object_info(env["obj"])

@route("/retrace/:num_steps")
def retrace_steps(num_steps):
    global env
    index = -int(num_steps)
    try:
        env["obj"] = env["trail"][index]
        del env["trail"][index]
    except IndexError:
        pass
    redirect("/")

@route("/static/:path#.+#")
def serve_static(path):
    return static_file(path, root="%s/static" % ROOT_DIR)

@route("/attr/:attr")
def view_attr(attr):
    global env
    # Save current object
    env["trail"].append(env["obj"])
    env["history"].append(env["obj"])
    # Set new object
    env["obj"] = getattr(env["obj"], attr)
    redirect("/")

@error(404)
def error404(error):
    return "Nothing here, sorry."


# START EXPLORING
def explore_object(obj=None):
    env["obj"] = obj

    debug(mode=True)
    run(host="localhost", port=8000, reloader=False)

if __name__ == "__main__":
    explore_object(Cat())
