from abc import ABC, abstractmethod


class Product(ABC):

    def __init__(self, name) -> None:
        self._name = name

    @abstractmethod
    def get_sample(self):
        raise NotImplementedError


class OnlineShop:

    def __init__(self) -> None:
        super().__init__()
        self._products = []

    def add_product(self, product):
        self._products.append(product)
        return self

    def get_samples(self):
        return [p.get_sample() for p in self._products]


class Book(Product):

    def get_sample(self):
        return self._name[0]


class Song(Product):

    def get_sample(self):
        return self._name[:3]


class Film(Product):

    def get_sample(self):
        return self._name[:5]