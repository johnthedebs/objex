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

    # This attribute is not consistent across PyPy, CPython 2.x,
    # and CPython 2.7
    exclude = set(['__abstractmethods__'])

    def __init__(self, obj):
        self.obj = obj

    def __unicode__(self):
        if hasattr(self.obj, "__unicode__"):
            return u"%s" % self.obj.__unicode__
        if hasattr(self.obj, "__name__"):
            return u"%s" % self.obj.__name__
        if hasattr(self.obj, "__class__"):
            return u"%s instance" % self.obj.__class__.__name__
        return u"%s" % type(self.obj)

    def get_attrs(self):
        attrs = [ (attr, self.get_attr_type(attr)) \
                    for attr in dir(self.obj)
                    if attr not in self.exclude ]
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

    def get_docstring(self):
        return inspect.getdoc(self.obj)

    def get_file(self):
        try:
            if inspect.isfunction(self.obj):
                return inspect.getsourcefile(self.obj)
            else:
                return inspect.getsourcefile(self.obj.__class__)
        except TypeError:
            # Error: Built-in module, class, or function.
            return ""

    @highlight_source
    def get_source(self):
        """
        Gets a given object's code. Works with module, class, method,
        function, traceback, frame, or code.
        """
        if self.obj in [object, type]:
            return 'builtin'
        elif inspect.isfunction(self.obj) or inspect.ismodule(self.obj) \
           or inspect.isclass(self.obj):
            return inspect.getsource(self.obj)
        try:
            return inspect.getsource(self.obj.__class__)
        except TypeError:
            # help() would be nice here but I haven't figured out how to
            # capture its output yet
            return ""

    def get_source_lines(self):
        return inspect.getsourcelines(self.obj)

    def get_parent_class_source(self):
        if inspect.isfunction(self.obj):
            return inspect.getsource(self.obj)
        return inspect.getsource(self.obj.__class__)

    def get_repr(self):
        return u"%s" % repr(self.obj)

    def get_source_file(self):
        if inspect.isfunction(self.obj):
            return inspect.getsourcefile(self.obj)
        return inspect.getsourcefile(self.obj.__class__)
