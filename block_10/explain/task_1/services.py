from datetime import date

from django.db import transaction

from block_10.explain.task_1.constants import RACKS_IN_HALL_COUNT, BOARDS_IN_RACK_COUNT, PLACES_ON_BOARD_COUNT
from block_10.explain.task_1.exceptions import EmptyPlaceDoesNotExist
from block_10.explain.task_1.models import Book, Author, PublicationType, BookCard, Hall, Board, Place, Rack, Placing, \
    Reader, LibraryCard
from block_10.explain.task_1.selectors import get_first_empty_place, get_book_current_placing


@transaction.atomic
def library_create(hall_count):
    for hall_number in range(1, hall_count+1):
        hall = Hall.objects.create(serial_number=hall_number)

        for rack_number in range(1, RACKS_IN_HALL_COUNT+1):
            rack = Rack.objects.create(hall=hall, serial_number=rack_number)

            for board_number in range(1, BOARDS_IN_RACK_COUNT+1):
                board = Board.objects.create(rack=rack, serial_number=board_number)

                for place_number in range(1, PLACES_ON_BOARD_COUNT+1):
                    Place.objects.create(board=board, serial_number=place_number)


@transaction.atomic
def book_add(name, authors, publication_types, isbn, number_pages, publication_date, description):
    book, created = Book.objects.get_or_create(
        isbn=isbn,
        defaults={
            'name': name,
            'number_pages': number_pages,
            'publication_date': publication_date,
            'description': description,
        }
    )

    if created:
        for author in authors:
            book.authors.add(Author.objects.get_or_create(name=author)[0])

        for pub_type in publication_types:
            book.publication_types.add(PublicationType.objects.get_or_create(name=pub_type)[0])

    card = BookCard.objects.create(book=book)
    book_place(card)

    return book


@transaction.atomic
def book_place(book_card):
    on_date = date.today()
    empty_place = get_first_empty_place(on_date)

    if empty_place:
        placing = Placing.objects.create(
            book_card=book_card,
            place=empty_place,
            begin_date=on_date,
        )
    else:
        raise EmptyPlaceDoesNotExist

    return placing


@transaction.atomic
def book_unplace(book_card):
    placing = get_book_current_placing(book_card)
    placing.end_date = date.today()
    placing.save()


@transaction.atomic
def book_give_to_reader(book_card, reader):
    # Проверить, есть ли такая книга в наличии
    pass
    # Проверить, может ли читатель взять книгу
    pass
    # Сделать запись в читательском билете
    pass
    # Снять книгу с текущего размещения
    book_unplace(book_card)


@transaction.atomic
def book_take_from_reader(book_card, reader):
    # Сделать запись в читательском билете
    pass
    # Проверить, не превышен ли срок хранения
    pass
    # Разместить книгу
    book_place(book_card)


@transaction.atomic
def reader_add(name):
    reader, created = Reader.objects.get_or_create(name=name)

    if created:
        LibraryCard.objects.create(reader=reader)

    return reader
