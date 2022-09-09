import os

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "course.settings")
django.setup()

from block_10.explain.task_1.services import (
    LibrarianManager,
    LibraryStorage,
    PreloaderBook,
)


if __name__ == '__main__':
    books_file = 'books.csv'

    # менеджер по работе с новыми книгами
    manager = LibrarianManager()
    # библиотечное хранилище, для добавления новых книг
    library_storage = LibraryStorage(manager=manager)

    # обработка файла с данными по книгам, для последующей загрузки книг в хранилище
    preload = PreloaderBook()
    preload.load_from_file(books_file)
    book_for_load = preload.get_load_books()

    # Добавление новых книг в библиотеку
    for book in book_for_load:
        library_storage.add(book)