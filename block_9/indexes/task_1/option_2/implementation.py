from django.db.models import (
    QuerySet,
    Q,
)

from .models import Employee


def filter_by_fio(fio) -> QuerySet:
    """Возвращает сотрудников, отфильтрованных по ФИО."""
    fio_list = fio.split(' ')
    fname = fio_list[0]
    iname = fio_list[1]
    oname = fio_list[2]

    queryset = Employee.objects.filter(fname=fname, iname=iname, oname=oname)

    return queryset


def filter_works_by_period(begin, end) -> QuerySet:
    """Возвращает сотрудников, работавших в заданном периоде хотя бы один день."""
    queryset = Employee.objects.filter(~Q(end__lte=begin) & ~Q(begin__gte=end))

    return queryset


def filter_by_country(country) -> QuerySet:
    """Возвращает сотрудников, отфильтрованных по стране."""
    queryset = Employee.objects.filter(country=country)

    return queryset


def filter_by_word_in_additional_info(word) -> QuerySet:
    """Возвращает сотрудников, отфильтрованных по слову в дополнительной информации."""
    #не получилось сделать c icontains, не заработал индекс

    queryset = Employee.objects.filter(Q(additional_info__contains=word) | Q(additional_info__contains=word.lower()))

    return queryset