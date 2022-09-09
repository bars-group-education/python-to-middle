import csv
import datetime
import re
from abc import ABC, abstractmethod
from itertools import product
from random import choice, randint
from typing import Union, List, Tuple, Dict



from block_10.explain.task_1.consts import NAMES
from block_10.explain.task_1.errors import FreePositionException
from block_10.explain.task_1.models import BookCard, LibraryHall, Librarian, \
    Shelf, Rack, BookStorage, Author, TypePublication


def get_random_name(suffix: str = '', choices: Union[list, tuple] = NAMES) -> str:
    """Получение случайного имени."""
    return f'{choice(choices).title()} {randint(1, 1000)}'


class AbstractProduct(ABC):
    """Абстрактный элемент описывающий создание продукта для библиотеки."""

    @abstractmethod
    def build(self, *args):
        """Создание продукта."""


class AbstractFactory(ABC):

    @abstractmethod
    def create_hall(self) -> AbstractProduct:
        """Создание помещения."""

    @abstractmethod
    def create_shelf(self) -> AbstractProduct:
        """Создание стеллажа."""

    @abstractmethod
    def create_rack(self) -> AbstractProduct:
        """Создание полки."""


class LibraryHallProduct(AbstractProduct):
    """Помещение библиотеки."""

    quantity = 1

    def build(self, librarian: Librarian) -> List[int]:
        """Создание помещения."""
        stor = []

        for _ in range(self.quantity):
            stor.append(
                LibraryHall(
                    name=get_random_name(
                        choices=('зал', 'офис', 'склад', 'холл')),
                    librarian=librarian,
                )
            )
        ids = LibraryHall.objects.bulk_create(stor)
        return ids


class LibraryShelfProduct(AbstractProduct):
    """Стеллаж в помещение."""

    quantity = 5

    def build(self, hall_ids: List[int]) -> List[int]:
        stor = []

        for hall_id in hall_ids:
            for _ in range(self.quantity):
                stor.append(
                    Shelf(
                        name=get_random_name(
                            choices=('стеллаж', 'шкаф')),
                        hall=hall_id,
                    )
                )
        ids = Shelf.objects.bulk_create(stor)
        return ids


class LibraryRackProduct(AbstractProduct):
    """Полка в стеллаж."""

    quantity = 6
    quantity_units = 10

    def build(self, shelf_ids: List[int]) -> Tuple[int, List[int]]:
        stor = []

        for shelf_id in shelf_ids:
            for _ in range(self.quantity):
                stor.append(
                    Rack(
                        name=get_random_name(
                            choices=('полка',)),
                        shelf=shelf_id,
                    )
                )
        ids = Rack.objects.bulk_create(stor)
        return ids, list(range(self.quantity_units))


class LibraryStorageFactory(AbstractFactory):
    """Создает определенные элементы хранилища."""

    def create_hall(self) -> AbstractProduct:
        """Добавление помещения."""
        return LibraryHallProduct()

    def create_shelf(self) -> AbstractProduct:
        """Добавление стеллажа."""
        return LibraryShelfProduct()

    def create_rack(self) -> AbstractProduct:
        """Добавление полок."""
        return LibraryRackProduct()


def create_hall(factory: AbstractFactory, librarian: Librarian):
    """Создание нового помещения."""
    hall = factory.create_hall()
    hall_ids = hall.build(librarian)
    shelf = factory.create_shelf()
    shelf_ids = shelf.build(hall_ids)
    rack = factory.create_rack()
    rack_ids = rack.build(shelf_ids)

    stor = []
    for hall_id, shelf_id, rack_id, position_id in product(hall_ids, shelf_ids, *rack_ids):
        stor.append(BookStorage(hall=hall_id, shelf=shelf_id, rack=rack_id, position=position_id))
    BookStorage.objects.bulk_create(stor)


class AbstractStorage(ABC):
    """Абстрактное хранилище."""

    @abstractmethod
    def add(self, *args):
        """Добавить в хранилище."""

    @abstractmethod
    def get(self, *args):
        """Получить из хранилища."""


class PreloaderBook:
    col_mapper = {
        'name': 'Название издания',
        'author': 'Авторы',
        'type_publication': 'Вид издания',
        'isbn': 'ISBN',
        'number_pages': 'Кол-во стр.',
        'date_publication': 'Год издания',
        'description': 'Аннотация',
    }

    def __init__(self):
        self._books = []
        self._is_normalize = False

    def load_from_file(self, filename):
        """Загрузка из файла."""
        with open(filename, 'r') as read_obj:
            csv_dict_reader = csv.DictReader(read_obj, delimiter='@', quotechar='#')
            for row in csv_dict_reader:
                self._books.append(
                    {k: row[v] for k, v in self.col_mapper.items()}
                )

    def _normalize(self):
        """Нормализация полученных данных."""
        for book in self._books:
            book['name'] = self._normalize_string(book['name'])
            book['author'] = self._normalize_author(
                self._normalize_string(book['author'])
            )
            book['type_publication'] = self._normalize_type_publication(
                self._normalize_string(book['type_publication'])
            )
            book['date_publication'] = self._normalize_date_publication(
                self._normalize_string(book['date_publication'])
            )
            book['description'] = self._normalize_string(book['description'])

        self._is_normalize = True

    def _normalize_string(self, string: str) -> str:
        return string.replace('\n', ' ').replace('  ', ' ')

    def _normalize_author(self, authors: str) -> List[str]:
        """Обработка строки со списком авторов."""
        pattern = r'(?P<author>\w+ \w\.\s?\w.)|(?P<author_a>\w\.\s?\w. \w+)'
        matchs = re.findall(pattern, authors, re.UNICODE)

        return [match[0] for match in matchs]

    def _normalize_date_publication(self, date_publication: str) -> datetime.date:
        """Приведение даты к формату даты"""
        return datetime.datetime.strptime(date_publication, '%Y').date()

    def _normalize_type_publication(self, type_publication: str) -> List[str]:
        """Обработка строки с типами публикаций,."""
        return type_publication.split(',')

    def get_load_books(self):
        """Возвращает список книг для дальнейшей обработки."""
        self._normalize()
        return self._books


class LibraryStorage(AbstractStorage):
    """Библиотечное хранилище."""

    def __init__(self, manager: 'LibrarianManager'):
        self._storage = []
        self.manager = manager

    def add(self, book: dict, *args):
        """Добавление данных о книге."""
        book_card = self.manager.add_bookcard(book)
        self._storage.append(book_card)

        self.manager.add_book(self.get())

    def get(self, *args) -> BookCard:
        """Получение карточки для последующего добавления книги."""
        item = None
        if self._storage:
            item = self._storage.pop()
        return item


class LibraryDirector:
    """Руководитель библиотеки.

    Отвечает за поиск новых библиотекарей и помещений.
    """

    def add_hall(self):
        """Добавление помещения."""
        librarian = self.add_librarian()
        create_hall(LibraryStorageFactory(), librarian)

    def add_librarian(self) -> Librarian:
        """Прием нового библиотекаря."""
        return Librarian.objects.create(
            name=get_random_name(choices=NAMES),
        )


class LibrarianManager:
    """Заведующий библиотекой."""

    director = LibraryDirector()

    def __init__(self):
        # Формат данных:
        #  key - помещение за которое отвечает сотрудник
        #  value - объект библиотекаря
        self.halls: Dict[int, LibraryWorker] = {}

        self._preload_halls()

    def add_bookcard(self, book: dict) -> BookCard:
        """Добавление карточки."""
        authors = book.pop('author', None)
        type_publications = book.pop('type_publication', None)
        book_card, _ = BookCard.objects.get_or_create(**book)

        for author in authors:
            a, _ = Author.objects.get_or_create(short_name=author)
            book_card.author.add(a)

        for type_publication in type_publications:
            tp, _ = TypePublication.objects.get_or_create(name=type_publication)
            book_card.type_publication.add(tp)

        book_card.save()

        return book_card

    def add_book(self, book_card: BookCard):
        """Разместить книгу на полке."""
        hall = BookStorage.get_first_free_hall()
        if not hall:
            self.director.add_hall()
            self._preload_halls()
            hall = BookStorage.get_first_free_hall()

        librarian = self.halls[hall.hall_id]
        librarian.put_book(book_card)

    def _preload_halls(self):
        """Обновление данных о помещениях библиотеки и ответственных сотрудниках."""
        self.halls = {
            hall.id: LibraryWorker(hall.librarian.name) for hall in LibraryHall.objects.all()
        }


class BaseLibraryWorker(ABC):
    """
    Базовый класс сотрудника библиотеки.

    Сотрудник занимается выдачей и получением книг.
    """

    @abstractmethod
    def get_book(self, *args):
        """Выдать книгу."""

    @abstractmethod
    def put_book(self, *args):
        """Положить книгу на полку."""


class LibraryWorker(BaseLibraryWorker):
    """Сотрудник библиотеки."""

    director = LibraryDirector()

    def __init__(self, name):
        self.name = name

    def get_book(self, book_card: BookCard):
        """Выдать книгу."""
        book = BookStorage.objects.get(book=book_card)

        return book.get_book()

    def put_book(self, book_card: BookCard):
        """Вернуть книгу."""
        try:
            BookStorage.put_book(book_card)
        except FreePositionException:
            self.director.add_hall()
            BookStorage.put_book(book_card)