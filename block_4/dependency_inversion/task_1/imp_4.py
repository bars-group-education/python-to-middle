from abc import abstractmethod


class OnlineShop:

    def __init__(self) -> None:
        super().__init__()
        self._cart = []

    def add_position(self, position):
        self._cart.append(position)

        return self

    def get_samples(self):
        return [
            b.get_fragment() for b in self._cart if isinstance(b, Fragment)
        ]


class CartPosition:

    @abstractmethod
    def get_sample(self):
        pass


class Fragment:

    @abstractmethod
    def get_fragment(self):
        pass


class Product:

    def __init__(self, name) -> None:
        super().__init__()
        self._name = name


class Book(Product, Fragment):

    def read_sample(self):
        return self._name[0]

    def get_fragment(self):
        return self.read_sample()


class Song(Product, Fragment):

    def listen_sample(self):
        return self._name[:3]

    def get_fragment(self):
        return self.listen_sample()


class Film(Product, Fragment):

    def see_segment(self):
        return self._name[:5]

    def get_fragment(self):
        return self.see_segment()