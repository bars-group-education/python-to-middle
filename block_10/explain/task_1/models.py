from datetime import date, datetime

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import (
    models,
)

from block_10.explain.task_1.constants import RACKS_IN_HALL_COUNT, BOARDS_IN_RACK_COUNT, PLACES_ON_BOARD_COUNT
from block_10.explain.task_1.enums import Location


class Person(models.Model):
    """Человек."""

    name = models.CharField(
        'ФИО',
        max_length=50,
    )

    class Meta:
        abstract = True


class Author(Person):
    """Автор."""


class PublicationType(models.Model):
    """Вид издания."""

    name = models.CharField(
        'Наименование',
        max_length=200,
    )


class Book(models.Model):
    """Книга."""

    name = models.CharField(
        'Название книги',
        max_length=100,
    )
    authors = models.ManyToManyField(
        Author,
        related_name='books',
        verbose_name='Авторы',
    )
    publication_types = models.ManyToManyField(
        PublicationType,
        related_name='books',
        verbose_name='Виды издания',
    )
    isbn = models.CharField(
        'Номер',
        max_length=25,
    )
    number_pages = models.SmallIntegerField(
        'Количество страниц',
    )
    publication_date = models.DateField(
        'Дата издания',
    )
    description = models.TextField(
        'Описание',
    )


class BookCard(models.Model):
    """Карточка книги."""

    number = models.CharField(
        'Номер',
        max_length=25,
        default=lambda: str(int(datetime.now().timestamp())),
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='cards',
        verbose_name='Книга',
    )


class Hall(models.Model):
    """Зал."""

    serial_number = models.SmallIntegerField(
        'Порядковый номер',
        validators=[MinValueValidator(1)],
    )


class Rack(models.Model):
    """Стеллаж."""

    serial_number = models.SmallIntegerField(
        'Порядковый номер',
        validators=[MinValueValidator(1), MaxValueValidator(RACKS_IN_HALL_COUNT)],
    )
    hall = models.ForeignKey(
        Hall,
        on_delete=models.CASCADE,
        related_name='racks',
        verbose_name='Зал',
    )


class Board(models.Model):
    """Полка."""

    serial_number = models.SmallIntegerField(
        'Порядковый номер',
        validators=[MinValueValidator(1), MaxValueValidator(BOARDS_IN_RACK_COUNT)],
    )
    rack = models.ForeignKey(
        Rack,
        on_delete=models.CASCADE,
        related_name='boards',
        verbose_name='Стеллаж',
    )


class Place(models.Model):
    """Место."""

    serial_number = models.SmallIntegerField(
        'Порядковый номер',
        validators=[MinValueValidator(1), MaxValueValidator(PLACES_ON_BOARD_COUNT)],
    )
    rack = models.ForeignKey(
        Rack,
        on_delete=models.CASCADE,
        related_name='boards',
        verbose_name='Стеллаж',
    )


class Placing(models.Model):
    """Размещение."""

    book_card = models.ForeignKey(
        BookCard,
        on_delete=models.CASCADE,
        related_name='entries',
        verbose_name='Карточка книги',
    )
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name='placings',
        verbose_name='Место',
    )
    begin_date = models.DateField(
        'Дата начала',
    )
    end_date = models.DateField(
        'Дата окончания',
        default=date.max,
    )


class Librarian(Person):
    """Библиотекарь."""


class Assignment(models.Model):
    """Назначение."""

    hall = models.ForeignKey(
        Hall,
        on_delete=models.CASCADE,
        related_name='assignments',
        verbose_name='Зал',
    )
    librarian = models.ForeignKey(
        Librarian,
        on_delete=models.CASCADE,
        related_name='assignments',
        verbose_name='Библиотекарь',
    )


class Reader(Person):
    """Читатель."""


class LibraryCard(models.Model):
    """Читательский билет."""

    reader = models.OneToOneField(
        Reader,
        on_delete=models.CASCADE,
        verbose_name='Читатель',
    )


class LibraryCardEntry(models.Model):
    """Запись в читательском билете."""

    library_card = models.ForeignKey(
        LibraryCard,
        on_delete=models.CASCADE,
        related_name='entries',
        verbose_name='Читательский билет',
    )
    book_card = models.ForeignKey(
        BookCard,
        on_delete=models.CASCADE,
        related_name='entries',
        verbose_name='Карточка книги',
    )
    location = models.PositiveSmallIntegerField(
        'Статус',
        choices=Location.choices,
    )
    issue_date = models.DateField(
        'Дата выдачи',
    )
    return_date = models.DateField(
        'Дата возврата',
        null=True,
    )

