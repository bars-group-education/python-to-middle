from django.db.models import (
    QuerySet,
)


def filter_by_fio(fio) -> QuerySet:
    """Возвращает сотрудников, отфильтрованных по ФИО."""
    raise NotImplementedError


def filter_works_by_period(begin, end) -> QuerySet:
    """Возвращает сотрудников, работавших в заданном периоде хотя бы один день."""
    raise NotImplementedError


def filter_by_country(country) -> QuerySet:
    """Возвращает сотрудников, отфильтрованных по стране."""
    raise NotImplementedError


def filter_by_word_in_additional_info(word) -> QuerySet:
    """Возвращает сотрудников, отфильтрованных по слову в дополнительной информации."""
    raise NotImplementedError