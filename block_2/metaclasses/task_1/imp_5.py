class Updateable(type):
    __class = None

    def __new__(cls, name, bases, kwargs):
        if not cls.__class:
            cls.__class = type.__new__(cls, name, bases, kwargs)
        return cls.__class

    def __init__(self, name, bases, kwargs):
        for attr_name, value in kwargs.items():
            if not (attr_name.startswith('__') and attr_name.endswith('__')):
                setattr(self, attr_name, value)