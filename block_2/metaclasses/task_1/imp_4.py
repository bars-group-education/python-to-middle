import weakref


class Updateable(type):
    _classes = []
    instances = []

    def __init__(self, name, bases, dict):
        self.__class__.instances.append(weakref.proxy(self))
        cls = super().__init__(self)
        return cls

    def __new__(self, name, bases, dict):

        if name not in self._classes:
            self._classes.append(name)
        else:
            for i in self.instances:
                if i.__name__ == name:
                    setattr(i, 'foo', dict['foo'])
        cls = super().__new__(self, name, bases, dict)
        return cls
