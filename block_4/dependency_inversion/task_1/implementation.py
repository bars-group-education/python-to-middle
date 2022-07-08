class Product:
    def __init__(self, name) -> None:
        super().__init__()
        self._name = name

    def get_sample(self):
        raise NotImplementedError


class OnlineShop:
    def __init__(self) -> None:
        super().__init__()
        self._products = []

    def add_product(self, item):
        self._products.append(item)

        return self

    def get_samples(self):
        return [product.get_sample() for product in self._products]


class Book(Product):

    def get_sample(self):
        return self._name[0]


class Song(Product):

    def get_sample(self):
        return self._name[:3]


class Film(Product):

    def get_sample(self):
        return self._name[:5]
