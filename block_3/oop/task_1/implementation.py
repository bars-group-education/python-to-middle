import json
from enum import Flag
from typing import Any


class ColumnAlreadyExist(Exception):
    pass


class RowAlreadyExist(Exception):
    pass


class DirectionSort(Flag):
    ASC = 1
    DESC = 2


class Column:
    def __init__(self, name, header) -> None:
        super().__init__()
        self._name = name
        self._hidden = False
        self._header = header
        self._filter = None

    @property
    def name(self):
        return self._name

    @property
    def filter_(self):
        return self._filter

    @filter_.setter
    def filter_(self, value):
        if not self._hidden:
            self._filter = value

    @property
    def hidden(self):
        return self._hidden

    def clear_filter(self):
        self.filter_ = None

    def hide(self):
        self._hidden = True
        self.clear_filter()

    def unhide(self):
        self._hidden = False


class ColumnStore:

    def __init__(self) -> None:
        super().__init__()
        self._clear_state()

    def _clear_state(self):
        self._columns = {}
        self._column_positions = []
        self._default_sort_column = 'id'
        self._sorted_column_name = ''
        self._sort_direction = DirectionSort.ASC

    @property
    def sort_params(self):
        return self._sorted_column_name, self._sort_direction

    def add(self, column):
        if column.name in self._column_positions:
            raise ColumnAlreadyExist(f'Колонка {column.name} уже существует')

        if not self._sorted_column_name and column.name == self._default_sort_column:
            self._sorted_column_name = column.name

        self._columns[column.name] = column
        self._column_positions.append(column.name)

    def move(self, name, position):
        self._column_positions.remove(name)
        self._column_positions.insert(position, name)

    def sort(self, name, direction=None):
        column = self._get_column(name)
        if not column.hidden:
            direction = direction or ~self._sort_direction
            self._sorted_column_name = f'{column.name}'
            self._sort_direction = direction

    def filter_(self, name, filter_value):
        column = self._get_column(name)
        column.filter_ = filter_value

    def hide(self, name):
        self._get_column(name).hide()

    def unhide(self, name):
        self._get_column(name).unhide()

    def load_data(self, data):
        self._clear_state()

        for row in data:
            for key in row:
                try:
                    self.add(Column(key, key))
                except ColumnAlreadyExist:
                    pass

    def get_visible_names(self):
        result = []

        for name in self._column_positions:
            if not self._get_column(name).hidden:
                result.append(name)

        return result

    def get_filters(self):
        return {x.name: x.filter_ for x in self._columns.values() if x.filter_ is not None}

    def _get_column(self, name):
        return self._columns[name]


class Row:

    def __init__(self, data) -> None:
        super().__init__()
        self._data = data

    def __getattr__(self, name: str) -> Any:
        if name in self._data:
            result = self._data[name]
        else:
            result = super().__getattribute__(name)

        return result


class RowStore:

    def __init__(self) -> None:
        super().__init__()
        self._clear_state()

    def _clear_state(self):
        self._rows = {}
        self._id_attr = 'id'
        self._selected_id = None
        self._deleted_ids = []

    @property
    def id_attr(self):
        return self._id_attr

    def add(self, row):
        id_ = getattr(row, self._id_attr)
        if id_ in self._rows:
            raise RowAlreadyExist(f'Строка с ключом {id_} уже существует')

        self._rows[id_] = row

    def get(self, id_):
        return self._rows[id_]

    def select(self, id_):
        if id_ in self._rows:
            self._selected_id = id_

    def delete(self, id_):
        if id_ in self._rows:
            self._deleted_ids.append(id_)

    def delete_selected(self):
        self.delete(self._selected_id)

    def load_data(self, data):
        self._clear_state()

        for row_data in data:
            self.add(Row(row_data))

    def all(self):
        for id_, row in self._rows.items():
            if id_ not in self._deleted_ids:
                yield row


class Table:
    def __init__(self) -> None:
        super().__init__()
        self._column_store = ColumnStore()
        self._row_store = RowStore()

    def load_data(self, data):
        data = json.loads(data)
        self._column_store.load_data(data)
        self._row_store.load_data(data)

    def export(self):
        filters = self._column_store.get_filters()
        sort_name, direction = self._column_store.sort_params
        for_sorting = []

        for row in self._row_store.all():
            for name, value in filters.items():
                if getattr(row, name) != value:
                    break
            else:
                for_sorting.append((
                    getattr(row, self._row_store.id_attr),
                    getattr(row, sort_name),
                ))

        for_sorting.sort(key=lambda x: x[1], reverse=direction == DirectionSort.DESC)

        result = []
        columns = self._column_store.get_visible_names()
        for id_, _ in for_sorting:
            row = self._row_store.get(id_)
            result.append({x: getattr(row, x) for x in columns})

        return result

    def add_column(self, column):
        self._column_store.add(column)

    def move_column(self, name, position):
        self._column_store.move(name, position)

    def sort(self, name, direction=None):
        self._column_store.sort(name, direction)

    def filter_(self, name, filter_value):
        self._column_store.filter_(name, filter_value)

    def hide(self, name):
        self._column_store.hide(name)

    def unhide(self, name):
        self._column_store.unhide(name)

    def add_row(self, row):
        self._row_store.add(row)

    def get_row(self, id_):
        return self._row_store.get(id_)

    def select_row(self, id_):
        self._row_store.select(id_)

    def delete_selected_row(self):
        self._row_store.delete_selected()
