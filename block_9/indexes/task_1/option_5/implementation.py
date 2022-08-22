from django.db.models import (
    QuerySet, Q,
)

from block_9.indexes.task_1.models import Employee


def filter_by_fio(fio: str) -> QuerySet:
    """Возвращает сотрудников, отфильтрованных по ФИО."""

    fname, iname, oname = fio.split(maxsplit=2)

    return Employee.objects.filter(fname=fname, iname=iname, oname=oname)


def filter_works_by_period(begin, end) -> QuerySet:
    """Возвращает сотрудников, работавших в заданном периоде хотя бы один день."""

    result = Employee.objects.filter(
        (Q(begin__lte=begin) & Q(end__gte=end))
        | (Q(begin__range=(begin, end)) & Q(end__gte=end))
        | (Q(begin__lte=begin) & Q(end__range=(begin, end)))
        | (Q(begin__gte=begin) & Q(end__lte=end))
    )

    return result


def filter_by_country(country) -> QuerySet:
    """Возвращает сотрудников, отфильтрованных по стране."""
    return Employee.objects.filter(country=country)


def filter_by_word_in_additional_info(word) -> QuerySet:
    """Возвращает сотрудников, отфильтрованных по слову в дополнительной информации."""
    return Employee.objects.filter(additional_info__icontains=word)