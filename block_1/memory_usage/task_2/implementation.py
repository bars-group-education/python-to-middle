class MyObject:

    def __init__(self, name) -> None:
        super().__init__()
        self.name = name


def cache(func):
    raise NotImplementedError


@cache
def create_object(name):
    return MyObject(name)
