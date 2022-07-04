class OnlineShop:

    def __init__(self) -> None:
        super().__init__()
        self._items = []

    def add_sample(self, item):
        self._items.append(item)

        return self

    def read_samples(self):
        return [i.get_sample() for i in self._items]


class Item:

    def __init__(self, name) -> None:
        super().__init__()
        self._name = name

    def get_sample(self):
        raise NotImplementedError


class Book(Item):

    def get_sample(self):
        return self._name[0]


class Song(Item):

    def get_sample(self):
        return self._name[:3]


class Film(Item):

    def get_sample(self):
        return self._name[:5]