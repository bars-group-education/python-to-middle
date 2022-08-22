from django.db.models import (
    QuerySet,
)

from block_9.indexes.task_1.models import Employee


def filter_by_fio(fio) -> QuerySet:
    """Возвращает сотрудников, отфильтрованных по ФИО."""
    fname, iname, *oname = fio.split()
    if oname:
        oname = ' '.join(oname)
    query = Employee.objects.filter(fname=fname, iname=iname, oname=oname)
    return query


def filter_works_by_period(begin, end) -> QuerySet:
    """Возвращает сотрудников, работавших в заданном периоде хотя бы один день."""
    query = Employee.objects.filter(begin__lte=end, end__gte=begin)
    return query


def filter_by_country(country) -> QuerySet:
    """Возвращает сотрудников, отфильтрованных по стране."""
    query = Employee.objects.filter(country=country)
    return query


def filter_by_word_in_additional_info(word) -> QuerySet:
    """Возвращает сотрудников, отфильтрованных по слову в дополнительной информации."""
    query = Employee.objects.filter(additional_info__icontains=word)
    return query