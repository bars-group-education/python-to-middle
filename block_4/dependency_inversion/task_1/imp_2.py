class Item:

    def __init__(self, name) -> None:
        super().__init__()
        self._name = name

    def get_semple(self):
        raise NotImplementedError


class OnlineShop:

    def __init__(self) -> None:
        super().__init__()
        self._items = []

    def add_book(self, item):
        if isinstance(item, Item):
            self._items.append(item)

        return self

    def read_samples(self):
        return [b.get_semple() for b in self._items]


class Book(Item):

    def get_semple(self):
        return self._name[0]


class Song(Item):

    def get_semple(self):
        return self._name[:3]


class Film(Item):

    def get_semple(self):
        return self._name[:5]