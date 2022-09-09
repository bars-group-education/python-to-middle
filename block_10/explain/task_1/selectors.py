from datetime import date

from block_10.explain.task_1.models import Book, Placing, Place


def get_first_empty_place(on_date):
    busy_places = Placing.objects.filter(
        begin_date__lte=on_date,
        end_date__gte=on_date,
    ).values_list(
        'place',
        flat=True,
    ).distinct()

    empty_place = Place.objects.exclude(
        pk__in=busy_places,
    ).order_by(
        'pk',
    ).first()

    return empty_place


def get_book_current_placing(book_card):
    return Placing.objects.get(
        book_card=book_card,
        end_date=date.max,
    )




