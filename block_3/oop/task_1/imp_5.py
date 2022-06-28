import json


class Column:
    """Столбец."""

    def __init__(self, header, type_) -> None:
        super().__init__()

        self.header = header
        self.hidden = False
        self.type = type_
        # от меньшего к большему, False - наоборот
        self.sorting_direction = True


class Row:
    """Запись таблицы, хранящая ссылки на свои столбцы."""

    def __init__(self, kwarg: dict, field_names: dict) -> None:
        """
        :param kwarg: словарь с полями записи
        """
        super().__init__()
        self.picked = False

        for key, value in kwarg.items():
            setattr(self, f'column_{key}', field_names.get(key))
            setattr(self, f'{key}', value)

    def delete(self):
        if self.picked:
            del self


class Table:
    """Таблица хранящая ссылки на список своих записей."""

    field_names = dict()
    rows = list()

    def load_data(self, data):

        data = json.loads(data)
        for key, value in data[0].items():
            column = Column(key, type(value))
            self.field_names[key] = column

        for row in data:
            row_obj = Row(row, self.field_names)
            self.rows.append(row_obj)

    def export(self):
        result = []
        for row in self.rows:
            row = {name: getattr(row, name) for name in self.field_names}
            result.append(row)
        return result

    def _get_column(self, column_name):
        """"""
        return self.field_names.get(column_name)

    def set_column_hidden(self, column_name):
        """Скрывает столбец."""

        column = self._get_column(column_name)
        column.hidden = True

    def do_swap_columns(self, column_name, index):
        """Пененосит указанный столбец в новое место."""

        pass

    def do_default_sort(self):
        """Сортирует сторки по id."""

        return self.rows.sort(key=lambda x: x.id)

    def do_sort(self, column_name):
        """Сортировка записей столбца."""

        column = self._get_column(column_name)

        if column.hidden:
            return

        column.sorting_direction = not column.sorting_direction

        return self.rows.sort(
            key=lambda x: getattr(x, column.header),
            reverse=not column.sorting_direction
        )

    def do_filter(self, column_name, search_str):
        """Фильтрация записей по столбцу."""

        column = self._get_column(column_name)
        result = []

        if not column.hidden:
            if column.type == str:
                search_str = str(search_str)
                result = list(
                    filter(
                        lambda x: search_str in getattr(
                            x, column_name
                        ), self.rows
                    )
                )

            elif column.type == int:
                search_str = int(search_str)
                result = list(
                    filter(lambda x: search_str == x, self.rows)
                )

            elif column.type == bool:
                search_str = bool(search_str)
                result = list(
                    filter(lambda x: search_str == x, self.rows)
                )
        return result