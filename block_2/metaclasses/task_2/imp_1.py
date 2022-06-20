class LazyMeta(type):
    def __call__(self, other):
        return other()

class Lazy(metaclass=LazyMeta):

    def __init__(self, expression) -> None:
        super().__init__()
        object.__setattr__(self, 'expression', expression)
