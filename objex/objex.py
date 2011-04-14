import code
import inspect
import pdb
import pyclbr
import symtable

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter


def highlight_source(func):
    """
    Decorator to highlight source coming from functions that return it.
    """
    def new_func(self, *args, **kwargs):
        source = func(self, *args, **kwargs)
        return highlight(source, PythonLexer(), HtmlFormatter())
    return new_func

class Objex(object):

    def __init__(self, obj):
        self.obj = obj

    def __unicode__(self):
        if hasattr(self.obj, "__name__"):
            return u"%s" % self.obj.__name__
        return u"%s" % type(self.obj)

    def get_attrs(self):
        attrs = [ (attr, self.get_attr_type(attr)) \
                    for attr in dir(self.obj) ]
        return attrs

    def get_attr_type(self, attr):
        return type( getattr(self.obj, attr) ).__name__

    def get_class_history(self, highlight=False):
        source_blobs = []
        for item in self.get_class_list():
            try:
                source_blobs.append(inspect.getsource(item))
            except TypeError:
                # TypeError for built-in objects. Skip 'em.
                continue
        return source_blobs

    def get_class_list(self, obj=None):
        """
        Returns a list consisting of an object's class and all of its
        base classes.

        If the object passed is a class, the list consists of that
        object and its base classes.
        """
        obj = obj or self.obj
        # If we don't have a class, get a class
        if type(obj) is not type:
            obj = obj.__class__
        objs = [obj]
        # Repeat this process recursively for all base classes
        for base in obj.__bases__:
            objs.extend( self.get_class_list(base) )
        return objs

    def get_class_name(self):
        return self.obj.__class__.__name__

    @highlight_source
    def get_class_source(self):
        return inspect.getsource(self.obj.__class__)

    @highlight_source
    def get_object_source(self):
        """
        Gets a given object's code. Works with module, class, method,
        function, traceback, frame, or code.
        """
        try:
            return inspect.getsource(self.obj)
        except TypeError:
            # help() would be nice, but for some reason this prints to the
            # terminal and causes problems...
            #return help(self.obj)
            return ""

    def get_parent_class_source(self):
        return inspect.getsource(self.obj.__class__)

    def get_source_file(self):
        return inspect.getsourcefile(self.obj.__class__)
