from django.db.models import (
    QuerySet, Q,
)

from block_9.indexes.task_1.models import Employee


def filter_by_fio(fio) -> QuerySet:
    """Возвращает сотрудников, отфильтрованных по ФИО."""
    f, i, o = fio.split()[:3]
    query = Employee.objects.filter(
        fname=f,
        iname=i,
        oname=o
    )
    print(query.explain())
    return query


def filter_works_by_period(begin, end) -> QuerySet:
    """Возвращает сотрудников, работавших в заданном периоде хотя бы один
    день. """

    return Employee.objects.filter(
        Q(begin__lte=begin, end__gte=begin) |
        Q(begin__gte=begin, end__lte=end) |
        Q(begin__gte=begin, begin__lte=end)
    )


def filter_by_country(country) -> QuerySet:
    """Возвращает сотрудников, отфильтрованных по стране."""
    return Employee.objects.filter(
        country=country
    )


def filter_by_word_in_additional_info(word) -> QuerySet:
    """Возвращает сотрудников, отфильтрованных по слову в дополнительной информации."""
    return Employee.objects.filter(
        additional_info__icontains=word
    )