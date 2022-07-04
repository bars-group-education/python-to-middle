from abc import ABC, abstractmethod


class Art(ABC):

    def __init__(self, name) -> None:
        super().__init__()
        self._name = name

    @abstractmethod
    def check_sample(self):
        pass


class OnlineShop:

    def __init__(self) -> None:
        super().__init__()
        self._piece_of_art = []

    def add_piece(self, piece):
        self._piece_of_art.append(piece)

        return self

    def check_samples(self):

        return [piece.check_sample() for piece in self._piece_of_art]


class Book(Art):

    def check_sample(self):

        return self._name[0]


class Song(Art):

    def check_sample(self):

        return self._name[:3]


class Film(Art):

    def check_sample(self):

        return self._name[:5]