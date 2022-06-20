SKIP_ATTRS = ['__name__', '__metaclass__', '__module__', '__dict__', '__weakref__', '__bases__']


class Updateable(type):

    def __new__(cls, name, bases, dct):
        module_name = dct['__module__']
        try:
            current_cls = registry[module_name][name]
        except KeyError:
            current_cls = None

        if current_cls:
            regenerate_class(current_cls, dct)
            new_cls = current_cls
        else:
            new_cls = type.__new__(cls, name, bases, dct)
            registry.setdefault(module_name, {})[name] = new_cls

        return new_cls


registry = {}


def regenerate_class(current_cls, dct):
    for name in list(current_cls.__dict__):
        if name in SKIP_ATTRS:
            continue

        delattr(current_cls, name)

    for name, value in dct.items():
        setattr(current_cls, name, value)

    return current_cls