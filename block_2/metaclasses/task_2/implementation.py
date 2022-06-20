import operator


def get_specials(some_type):
    return [x for x in dir(some_type) if x.startswith('__') and x not in SKIP_ATTRS]


SKIP_ATTRS = ['__new__', '__init__', '__class__']
SPECIALS = set(get_specials(str) + get_specials(int) + get_specials(list) + get_specials(dict))


class LazyMeta(type):

    @classmethod
    def __prepare__(cls, name, bases):
        methods = {}

        for method_name in SPECIALS:
            methods[method_name] = cls.get_method(method_name)

        return methods

    def get_method(method_name):

        def method(self, *args, **kwargs):
            try:
                value = object.__getattribute__(self, 'value')
            except AttributeError:
                value = object.__getattribute__(self, 'expression')()
                object.__setattr__(self, 'value', value)

            if method_name in operator.__dict__:
                result = getattr(operator, method_name)(value, *args, **kwargs)
            else:
                result = getattr(value, method_name)(*args, **kwargs)

            return result

        return method


class Lazy(metaclass=LazyMeta):
    def __init__(self, expression) -> None:
        super().__init__()
        object.__setattr__(self, 'expression', expression)