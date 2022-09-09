from typing import Optional

from django.db import (
    models, transaction,
)

from block_10.explain.task_1.errors import TakeBookException, \
    FreePositionException


class BookInstanceStatus(models.TextChoices):
    """Статус книги."""

    AVAILABLE = 1, 'Доступна'
    MISSING = 2, 'Отсутствует'


class BookMovementStatus(models.TextChoices):
    """Статус книги в журнале."""

    ISSUED = 1, 'Выдана'
    RETURNED = 2, 'Возвращена'
    MOVEMENT = 3, 'Перемещена'


class Author(models.Model):
    """Автор."""

    short_name = models.CharField(
        'Автор книги',
        max_length=50,
        unique=True,
    )

    class Meta:
        db_table = 'library_author'
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class TypePublication(models.Model):
    """Тип издания."""

    name = models.CharField(
        'Тип издания',
        max_length=200,
        unique=True,
    )

    class Meta:
        db_table = 'library_typepublication'
        verbose_name = 'Тип издания'
        verbose_name_plural = 'Типы изданий'


class BookCard(models.Model):
    """Книга."""

    name = models.CharField('Название книги', max_length=255)
    author = models.ManyToManyField(
        Author,
        related_name='books',
        verbose_name='Авторы',
    )
    type_publication = models.ManyToManyField(
        TypePublication,
        related_name='type_publications',
        verbose_name='Тип издания',
    )
    isbn = models.CharField(
        'Номер',
        max_length=25,
    )
    number_pages = models.SmallIntegerField('Количество страниц')
    date_publication = models.DateField('Дата публикации')
    description = models.TextField('Описание')
    status = models.PositiveSmallIntegerField(
        'Статус',
        choices=BookInstanceStatus.choices,
        default=BookInstanceStatus.AVAILABLE,
    )

    class Meta:
        db_table = 'library_bookcard'
        verbose_name = 'Книжная карточка'
        verbose_name_plural = 'Книжные карточки'


class Reader(models.Model):
    """Читатель."""

    name = models.CharField(
        'Наименование',
        max_length=50,
    )

    class Meta:
        db_table = 'library_reader'
        verbose_name = 'Читатель'
        verbose_name_plural = 'Читатели'


class Librarian(models.Model):
    """Библиотекарь."""

    name = models.CharField(
        'Наименование',
        max_length=100,
    )

    class Meta:
        db_table = 'library_librarian'
        verbose_name = "Библиотекарь"
        verbose_name_plural = "Библиотекари"


class ReaderTicket(models.Model):
    """Читательский билет."""

    reader = models.ForeignKey(
        Reader,
        on_delete=models.CASCADE,
        related_name='ticket',
        verbose_name='Читатель',
    )
    book = models.ForeignKey(
        BookCard,
        on_delete=models.CASCADE,
        verbose_name='Книга'
    )
    date_issue = models.DateField(
        'Дата выдачи книги',
    )
    date_return = models.DateField(
        'Дата возврата книги',
        null=True,
    )
    is_out_time = models.BooleanField(
        'Книга возвращена не во время',
        default=False,
    )

    class Meta:
        db_table = 'library_readerticket'
        verbose_name = 'Читательский билет'
        verbose_name_plural = 'Читательские билеты'


class LibraryHall(models.Model):
    """Библиотечный зал."""

    name = models.CharField(
        'Наименование зала',
        max_length=25,
    )
    librarian = models.OneToOneField(
        Librarian,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Закрепленный библиотекарь',
    )

    class Meta:
        db_table = 'library_libraryhall'
        verbose_name = 'Библиотечный зал'
        verbose_name_plural = 'Библиотечные залы'

    def __str__(self):
        return self.name


class Shelf(models.Model):
    """Стеллаж."""

    name = models.CharField(
        'Наименование стеллажа',
        max_length=25,
    )
    hall = models.ForeignKey(
        LibraryHall,
        on_delete=models.CASCADE,
        related_name='shelfs',
        verbose_name='Зал',
    )

    class Meta:
        db_table = 'library_shelf'
        verbose_name = 'Стеллаж'
        verbose_name_plural = 'Стеллажи'

    def __str__(self):
        return f'{self.hall}/{self.name}'


class Rack(models.Model):
    """Полка в стеллаже."""

    name = models.CharField(
        'Наименование полки',
        max_length=25,
    )
    shelf = models.ForeignKey(
        Shelf,
        on_delete=models.CASCADE,
        related_name='racks',
        verbose_name='Стеллаж',
    )

    class Meta:
        db_table = 'library_rack'
        verbose_name = 'Полка'
        verbose_name_plural = 'Полки'

    def __str__(self):
        return f'{self.shelf}/{self.number}'


class BookStorage(models.Model):
    """Хранилище книг."""

    hall = models.ForeignKey(
        LibraryHall,
        on_delete=models.PROTECT,
        related_name='books',
        verbose_name='Книжный зал',
    )
    shelf = models.ForeignKey(
        Shelf,
        on_delete=models.PROTECT,
        related_name='books',
        verbose_name='Номер стеллажа',
    )
    rack = models.ForeignKey(
        Rack,
        on_delete=models.PROTECT,
        related_name='books',
        verbose_name='Номер полки',
    )
    position = models.PositiveSmallIntegerField(
        'Позиция книги на полке',
    )
    book = models.ForeignKey(
        BookCard,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Карточка',
    )

    class Meta:
        db_table = 'library_bookstorage'
        verbose_name = 'Книга в наличии'
        verbose_name_plural = 'Книги в наличии'

    @classmethod
    def get_first_free_position(cls):
        """Получение первого свободного места для размещения книги."""
        return cls.objects.filter(book__isnull=True).first()

    @classmethod
    def get_first_free_hall(cls) -> Optional[int]:
        """Получение идентификатора помещения где есть свободная полка."""
        return cls.objects.filter(book__isnull=True).first()

    def get_librarian(self):
        """Возвращает ответственного библиотекаря."""
        return self.hall.librarian

    @classmethod
    def put_book(cls, card_book: BookCard):
        with transaction.atomic():
            free_position = cls.get_first_free_position()
            if not free_position:
                raise FreePositionException('Свободныйх мест для книг нет.')
            position = cls.objects.select_for_update().get(pk=free_position.id)
            position.book = card_book
            position.save()

    def get_book(self):
        """Получить книгу."""
        if self.book is None:
            raise TakeBookException('Книгу уже забрали')

        return self.take_book(self.pk)

    @classmethod
    def take_book(cls, _id: int) -> 'BookCard':
        """Выдача книги."""
        with transaction.atomic():
            take_book: BookStorage = cls.objects.select_for_update().get(pk=_id)
            book: BookCard = take_book.book

            take_book.book = None
            take_book.save()
            return book


class BookMovementLog(models.Model):
    """Журнал перемещения книг."""

    book = models.ForeignKey(
        BookStorage,
        on_delete=models.CASCADE,
        verbose_name='Книга',
    )
    reader = models.ForeignKey(
        Reader,
        on_delete=models.CASCADE,
        verbose_name='Читатель',
        null=True,
    )
    librarian = models.ForeignKey(
        Librarian,
        on_delete=models.CASCADE,
        verbose_name='Библиотекарь',
        null=True,
    )
    rack = models.ForeignKey(
        Rack,
        on_delete=models.RESTRICT,
        verbose_name='Полка',
        null=True,
    )
    status = models.PositiveSmallIntegerField(
        'Статус',
        choices=BookMovementStatus.choices,
    )

    class Meta:
        db_table = 'library_bookmovementlog'
        verbose_name = verbose_name_plural = 'Журнал перемещения книг'