class Lazy(metaclass=LazyMeta):
    def __init__(self, expression) -> None:
        super().__init__()
        object.__setattr__(self, 'expression', expression)