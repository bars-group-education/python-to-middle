from django.db.models import (
    QuerySet,
)

from block_9.indexes.task_1.models import (
    Employee,
)


def filter_by_fio(fio) -> QuerySet:
    """Возвращает сотрудников, отфильтрованных по ФИО.

    Index Scan using fio_idx on public.indexes_employees  (cost=0.41..8.43 rows=1 width=111) (actual time=0.028..0.035 rows=0 loops=1)
      Output: id, inn, fname, iname, oname, country, department_id, position_id, begin, "end", additional_info
      Index Cond: ((((((indexes_employees.fname)::text || ' '::text) || (indexes_employees.iname)::text) || ' '::text) || (indexes_employees.oname)::text) = 'Иванов Иван Иванович'::text)
    Planning Time: 0.192 ms
    Execution Time: 0.082 ms
    """
    return Employee.objects.extra(
        where=["fname || ' ' || iname || ' ' || oname = %s"],
        params=[fio],
    )


def filter_works_by_period(begin, end) -> QuerySet:
    """Возвращает сотрудников, работавших в заданном периоде хотя бы один день."""
    return Employee.objects.filter(begin__lte=end, end__gte=begin)


def filter_by_country(country) -> QuerySet:
    """Возвращает сотрудников, отфильтрованных по стране."""
    return Employee.objects.filter(country=country)


def filter_by_word_in_additional_info(word) -> QuerySet:
    """Возвращает сотрудников, отфильтрованных по слову в дополнительной информации."""
    return Employee.objects.filter(additional_info__icontains=word)