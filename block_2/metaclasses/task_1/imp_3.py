class Updateable(type):
    _instance = None

    def __init__(self, name, bases, namespace):
        super().__init__(name, bases, namespace)
        for name, val in namespace.items():
            if callable(val):
                setattr(self, name, val)

    def __new__(cls, name, bases, namespace):
        if not cls._instance:
            cls._instance = super().__new__(cls, name, bases, namespace)
        return cls._instance