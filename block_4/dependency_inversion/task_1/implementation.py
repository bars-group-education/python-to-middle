class OnlineShop:

    def __init__(self) -> None:
        super().__init__()
        self._books = []

    def add_book(self, book):
        self._books.append(book)

        return self

    def read_samples(self):
        return [b.read_sample() for b in self._books]


class Book:

    def __init__(self, name) -> None:
        super().__init__()
        self._name = name

    def read_sample(self):
        return self._name[0]


class Song:

    def __init__(self, name) -> None:
        super().__init__()
        self._name = name

    def listen_sample(self):
        return self._name[:3]


class Film:

    def __init__(self, name) -> None:
        super().__init__()
        self._name = name

    def see_segment(self):
        return self._name[:5]
