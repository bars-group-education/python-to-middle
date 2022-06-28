import json
from collections import namedtuple
from operator import attrgetter
from typing import Callable
from typing import Iterable
from typing import Optional


sorting = namedtuple('sorting', ['name', 'reverse'])


def validate_column_name(method: Callable):
    def wrapper(self, *args, **kwargs):
        for arg in args:
            if arg not in self._columns:
                raise ValueError(f'Неверно указан заголовок столбца: {arg}')
        return method(self, *args, **kwargs)

    return wrapper


class Column:
    def __init__(self, name: str) -> None:
        self.name = name

        self.max_length = 0
        self.hidden = False
        self.filter_ = None

    def set_filter(self, func):
        self.filter_ = func


class Row:
    def __init__(self, data: dict) -> None:
        self.__dict__.update(data)
        self.selected = False


class Table:
    def __init__(self) -> None:
        self.sorting: Optional[sorting] = None
        self._columns: dict[str, Column] = {}
        self._column_positions: list[str] = []
        self._rows: list[Row] = []

    def load_data(self, data):
        json_data = json.loads(data)
        for row in json_data:
            self._rows.append(Row(row))
            for name in row:
                if name not in self._columns:
                    self._columns[name] = Column(name)
                column_max_length = len(
                    str(row[name]) if row[name] is not None else 'None'
                )
                if column_max_length > self._columns[name].max_length:
                    self._columns[name].max_length = column_max_length
        for column in self._columns:
            self._column_positions.append(column)

    def export(self):
        return json.dumps(self.prepare())

    @property
    def _sorted_rows(self):
        return (
            self._rows
            if not self.sorting
            else sorted(
                self._rows,
                key=attrgetter(self.sorting.name),
                reverse=self.sorting.reverse,
            )
        )

    @property
    def _visible_columns(self) -> Iterable[str]:
        return filter(
            lambda name: not self._columns[name].hidden,
            self._column_positions,
        )

    def render(self) -> None:
        for row in self.prepare():
            row_text = ''
            for column_name in self._visible_columns:
                column = self._columns[column_name]
                cell_value = row[column_name]
                row_text += (
                    f'| {str(cell_value):{column.max_length}} '
                    if cell_value is not None
                    else '| None '
                )
            print(row_text, end='|\n')

    def prepare(self) -> list:
        result = []
        for row in self._sorted_rows:
            obj = {}
            skip = False
            for column_name in self._visible_columns:
                column = self._columns[column_name]
                cell_value = getattr(row, column.name)
                if column.filter_ and not column.filter_(cell_value):
                    skip = True
                    break
                obj[column_name] = cell_value
            if not skip:
                result.append(obj)
        return result

    @validate_column_name
    def switch_columns(self, name1: str, name2: str) -> None:
        name1_index = self._column_positions.index(name1)
        name2_index = self._column_positions.index(name2)
        self._column_positions[name1_index] = name2
        self._column_positions[name2_index] = name1

    @validate_column_name
    def hide(self, column_name) -> None:
        self._columns[column_name].hidden = True
        if self.sorting and self.sorting.name == column_name:
            self.sorting = None

    @validate_column_name
    def set_filter(self, column_name, *, func=None) -> None:
        self._columns[column_name].set_filter(func)

    @validate_column_name
    def set_sorting(self, column_name, *, reverse=False) -> None:
        if self._columns[column_name].hidden:
            raise ValueError('Скрытый столбец нельзя сортировать')
        self.sorting = sorting(column_name, reverse)

    def select_row(self, number: int) -> None:
        if 0 > number > len(self.prepare()) - 1:
            raise ValueError('Укажите корректный номер строки')
        self._rows[number].selected = True

    def delete_row(self) -> None:
        self._rows = list(filter(lambda row: row.selected, self._rows))


if __name__ == '__main__':
    table = Table()
    with open('data/data.json', 'r') as f:
        table.load_data(f.read())

    table.hide('alternate_name')
    table.switch_columns('id', 'group_letter')
    table.set_filter('group_letter', func=lambda value: value == 'D')
    table.set_sorting('id')
    table.render()
    print(table.export())