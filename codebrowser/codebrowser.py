import code
import inspect
import pdb
import pyclbr
import symtable


class CodeBrowser(object):
    def __init__(self, obj):
        self.obj = obj

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
        obj = obj or self.obj
        # If we don't have a class, get a class
        if type(obj) is not type:
            obj = obj.__class__
        objs = [obj]

        for base in obj.__bases__:
            objs.extend( self.get_class_list(base) )

        return objs

    def get_class_name(self):
        return self.obj.__class__.__name__

    def get_class_source(self):
        return inspect.getsource(self.obj.__class__)

    def get_object_source(self):
        return inspect.getsource(self.obj)

    def get_parent_class_source(self):
        return inspect.getsource(self.obj.__class__)

    def get_source_file(self):
        return inspect.getsourcefile(self.obj.__class__)
