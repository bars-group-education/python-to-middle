import json
from dataclasses import dataclass
from operator import attrgetter
from typing import List, Callable, Any, Dict, Union


@dataclass
class Sort:
    field: str
    reverse: bool


class Row:
    """Строка с данными."""

    def __init__(self, data: dict):
        for attr, value in data.items():
            setattr(self, attr, value)

    def __repr__(self):
        return f'Row<{self.__dict__}>'


class ISelect:
    _select = False

    def is_select(self):
        return self._select

    def select(self):
        """
        Выделение элемента.

        Если у выделенного элемента повторно вызвать метод,
        то выделение будет снято.
        """
        self._select = not self._select


class TableRow(Row, ISelect):
    """Строка в таблице."""


class Column:
    """Колонка."""

    def __init__(self, name):
        self.name = name


class TableColumn(Column):
    """Колонка в таблице."""

    def __init__(self, table, name):
        super().__init__(name)

        self._table = table
        self._filter = None
        self._sort = None
        self._visible = True

    @property
    def visible(self):
        return self._visible

    def hide(self):
        """
        Сделать скрытой.

        При скрытии сбрасываются сортировка и фильтр.
        """
        self._visible = False
        self._filter = None
        self._sort = None

    def show(self):
        """Сделать видимой."""
        self._visible = True

    def set_sorting(self, reverse: bool):
        """Применить сортировку."""
        self._sort = Sort(self.name, reverse)


class Table:
    def __init__(self):
        self._rows = []
        self._rows_select = []
        self._column_names = []
        self._columns = {}
        self._default_sorts = (Sort('id', False),)

    @property
    def columns(self) -> Dict[str, TableColumn]:
        """Возвращает колонки."""
        return self._columns

    @property
    def rows(self) -> List[TableRow]:
        """Возвращает строки."""
        return self._rows

    def load_data(self, data: str):
        """Загрузка данных в таблицу."""
        for row in json.loads(data):
            self.add_row(row)

    def add_row(self, data: dict):
        """Добавить строку."""
        _row = TableRow(data)
        for col_name in data:
            self.add_column(col_name)
        self._rows.append(_row)

    def add_column(self, name):
        """Добавить колонку."""
        if name not in self._column_names:
            self._columns[name] = TableColumn(self, name)
            self._column_names.append(name)

    def get_row(self, _id):
        """Получение строки по id (порядковому номеру в списке)."""
        if _id < 0 or _id > len(self._rows):
            assert ValueError('Строка не существует')

        return self._rows[_id]

    def get_column(self, name: str) -> TableColumn:
        """Возвращает колонку по наименованию."""
        if name not in self._columns:
            raise KeyError(f'Колонка {name} не найдена')

        return self._columns[name]

    def row_select(self, _id: int):
        """Установить/снять выделение со строку(и)."""
        self.get_row(_id).select()

    def remove_select(self):
        """Удаление выделенных строк."""
        self._rows = [row for row in self._rows if not row.is_select()]

    def col_hide(self, col_name: str):
        """Скрыть колонку."""
        self.get_column(col_name).hide()

    def col_show(self, col_name: str):
        """Сделать колонку не скрытой."""
        self.get_column(col_name).show()

    def swap_columns(self, l_name, r_name):
        """Смена колонок местами."""
        if l_name not in self._column_names or r_name not in self._column_names:
            raise ValueError(
                'Передано некорректное наименование одной из колонок'
            )

        c_names = self._column_names
        lid = c_names.index(l_name)
        rid = c_names.index(r_name)
        c_names[lid], c_names[rid] = r_name, l_name

    def set_filter(self, col_name: str, func: Callable[..., Any]):
        """Установка фильтра на колонку."""
        column = self.get_column(col_name)
        if not column.visible:
            raise KeyError('Скрытая колонка не поддерживает данное действие')
        column._filter = func

    def set_sorting(self, col_name: str, reverse: bool = False):
        """Сортировка колонки."""
        column = self.get_column(col_name)
        if not column.visible:
            raise KeyError('Скрытая колонка не поддерживает данное действие')
        column.set_sorting(reverse)

    def export_row(self, row: TableRow, column_names: list):
        """Экспортирует строку."""
        return {col_name: getattr(row, col_name) for col_name in column_names}

    def _get_rows(self):
        """Получение строк с применением фильтра и сортировки"""
        _rows = self._get_filtred_rows(self.rows, self._get_filter())
        _rows = self._get_sorted_rows(_rows, self._get_sort())

        return _rows

    def _get_filtred_rows(self, rows: List[TableRow],
                          filters: Dict[str, Callable[..., Any]]
                          ) -> List[TableRow]:
        """Возвращает отфильтрованные строки."""
        _rows = []
        if filters:
            for row in rows:
                if all(
                    _filter(getattr(row, col_name))
                    for col_name, _filter in filters.items()
                ):
                    _rows.append(row)
        else:
            _rows = rows

        return _rows

    def _get_filter(self) -> Dict[str, Callable[..., Any]]:
        """Возвращает наименование колонки и фильтр для нее."""
        return {
            col_name: column._filter
            for col_name, column in self.columns.items()
            if column.visible and column._filter
        }

    def _get_sorted_rows(self, rows, _sorted: Union[List[Sort], list]):
        """Возвращает отсортированные строки."""
        if not _sorted:
            _sorted = self._default_sorts
        for _sort in reversed(_sorted):
            rows = sorted(
                rows, key=attrgetter(_sort.field), reverse=_sort.reverse
            )

        return rows

    def _get_sort(self) -> Union[List[Sort], list]:
        """Получение примененных правил сортировки с колонок."""
        return [
            column._sort for column in self.columns.values()
            if column.visible and column._sort
        ]

    def export(self) -> str:
        """Возвращает список данных таблицы."""
        column_names = [
            col_name for col_name in self._column_names
            if self.get_column(col_name).visible
        ]
        result = [
            self.export_row(row, column_names) for row in self._get_rows()
        ]

        return json.dumps(result)


if __name__ == '__main__':
    table = Table()
    with open('data/data.json', 'r') as f:
        table.load_data(f.read())
    table.set_filter('group_letter', func=lambda value: value == 'B')
    table.set_filter('id', func=lambda value: value == 6)
    table.set_sorting('group_letter', reverse=True)
    e = table.export()