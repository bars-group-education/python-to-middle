import inspect
from unittest import TestCase

from block_4.dependency_inversion.task_1.implementation import OnlineShop, Book, Song, Film


class Test(TestCase):


    def setUp(self) -> None:
        super().setUp()
        self.shop = OnlineShop()

        for name, method in inspect.getmembers(self.shop, predicate=inspect.ismethod):
            if name.startswith('add_'):
                self.add_to_shop = method
            elif name.endswith('_samples'):
                self.get_samples = method

    def test_book(self):
        self.add_to_shop(Book('Гарри Поттер'))
        self.add_to_shop(Book('Город женщин'))
        self.add_to_shop(Book('Мастер и Маргарита'))

        self.assertEqual(self.get_samples(), ['Г', 'Г', 'М'])

    def test_song(self):
        self.add_to_shop(Song('Comatose'))
        self.add_to_shop(Song('Город'))
        self.add_to_shop(Song('Волкодав'))

        self.assertEqual(self.get_samples(), ['Com', 'Гор', 'Вол'])

    def test_film(self):
        self.add_to_shop(Film('Время первых'))
        self.add_to_shop(Film('Легенда 17'))
        self.add_to_shop(Film('Звездная пыль'))

        self.assertEqual(self.get_samples(), ['Время', 'Леген', 'Звезд'])

    def test_mix(self):
        self.add_to_shop(Book('Тайный город'))
        self.add_to_shop(Song('Папа What\'s Up'))
        self.add_to_shop(Film('Перед рассветом'))

        self.assertEqual(self.get_samples(), ['Т', 'Пап', 'Перед'])