from abc import ABC, abstractmethod


class Item(ABC):
    def __init__(self, name) -> None:
        super().__init__()
        self._name = name

    @abstractmethod
    def get_sample(self):
        raise NotImplementedError


class OnlineShop:

    def __init__(self) -> None:
        super().__init__()
        self._items = []

    def add_item(self, item):
        self._items.append(item)

        return self

    def get_samples(self):
        return [item.get_sample() for item in self._items]


class Book(Item):

    def get_sample(self):
        return self._name[0]


class Song(Item):

    def get_sample(self):
        return self._name[:3]


class Film(Item):

    def get_sample(self):
        return self._name[:5]