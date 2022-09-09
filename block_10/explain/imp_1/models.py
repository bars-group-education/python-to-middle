from django.db import models


class Book(models.Model):
    """
    Модель книги
    """
    name = models.CharField('Название книги', max_length=100, default='')

    class Meta:
        verbose_name = 'Книга'


class Publisher(models.Model):
    name = models.CharField('Название издательства')

    class Meta:
        verbose_name = 'Вид издания'


class Author(models.Model):
    """
    Автор книги
    """
    name = models.CharField("Имя автора", max_length=100, default='')

    class Meta:
        verbose_name = 'Автор'


class LibraryRoom(models.Model):
    """
    Зал библиотеки
    """
    name = models.CharField('Название зала', max_length=100, null=False)

    class Meta:
        verbose_name = 'Зал библиотеки'


class Librarian(models.Model):
    """
    Модель библиотекоря
    """
    name = models.CharField('Имя библиотекоря', max_length=100, null=False)
    vacation = models.BooleanField('Отпуск', default=False)
    library_room = models.ManyToManyField(LibraryRoom, related_name='librarian', db_table='library_rooms_librarian')

    class Meta:
        verbose_name = 'Библиотекорь'


class Closet(models.Model):
    """
    Модель стелажа
    """
    unique_number = models.IntegerField('Уникальный номер стелажа', null=False)
    library_room = models.ForeignKey(LibraryRoom, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Стелаж'


class Shelf(models.Model):
    """
    Модель полки в стелаже
    """
    shelf_number = models.IntegerField('Номер полки', null=False)
    closet = models.ForeignKey(Closet, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Полка в стелаже'


class BookCard(models.Model):
    """
    Модель карточки для книги
    """
    book = models.OneToOneField(Book, on_delete=models.CASCADE)
    author = models.ManyToManyField(Author, related_name='author', db_table='books_author')
    publisher = models.ForeignKey(Publisher, related_name='publisher', on_delete=models.PROTECT)
    inventory_number = models.IntegerField('Инвентарный номер', null=False)
    pages_number = models.PositiveIntegerField('Количество страниц', null=False)
    description = models.TextField('Описание', default='')
    shelf = models.ForeignKey(Shelf, on_delete=models.PROTECT, null=True)
    taken = models.BooleanField('Книга взята читателем', default=False)
    taken_by =

    class Meta:
        verbose_name = 'Карточка для книги'

    @property
    def book_name(self):
        """Получение названия книги"""
        return self.book.name


class ReaderCard(models.Model):
    """Класс карточки читателя"""
    reader_name = models.CharField()
    book

class Journal(models.Model):
    """
    Журнал для записи перемещения книг между стеллажами
    """
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    from_shelf = models.ForeignKey(Shelf, on_delete=models.PROTECT)
    to_shelf = models.ForeignKey(Shelf, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Журнал записи перемещения книг'