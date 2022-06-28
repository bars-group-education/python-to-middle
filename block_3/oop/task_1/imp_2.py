from abc import ABCMeta, abstractmethod
import json


class Interface(metaclass=ABCMeta):
    """Интерфейс взаимодействия"""

    @abstractmethod
    def load_data(self, data):
        raise NotImplementedError

    @abstractmethod
    def export(self):
        raise NotImplementedError

    @abstractmethod
    def sort_column(self, column_name, reverse=False):
        raise NotImplementedError

    @abstractmethod
    def hidden_column(self, column_name):
        raise NotImplementedError

    @abstractmethod
    def change_position(self, column_name_first, column_name_second):
        raise NotImplementedError

    @abstractmethod
    def select_row(self, row_id):
        raise NotImplementedError

    @abstractmethod
    def delete_selected_rows(self):
        raise NotImplementedError


class Row:
    """
    Класс строки таблицы
    """

    __sort_id = None

    def set_sort_id(self, sort_id):
        self.__sort_id = sort_id

    def get_sort_id(self):
        return self.__sort_id

    def init_attributes(self, attr):
        for key, value in attr.items():
            setattr(self, key, value)

    def get_attrs(self):
        class_attr = set([m for m in dir(Row) if not m.startswith('__')])
        object_attr = set([m for m in dir(self) if not m.startswith('__')])
        attributes = list(object_attr - class_attr)
        attributes.sort()

        return attributes


class Table(Interface):
    """Класс таблицы"""

    __rows = []
    __columns = []
    __hidden_columns = []
    __selected_rows = []

    def load_data(self, data):
        data_json = json.loads(data)
        for i, row in enumerate(data_json, 1):
            new_row = Row()
            new_row.init_attributes(row)
            new_row.set_sort_id(i)
            columns = new_row.get_attrs()
            self.__check_columns(columns)
            self.__rows.append(new_row)

    def __check_columns(self, columns):
        for column in columns:
            if column not in self.__columns:
                self.__add_column(column)

    def __add_column(self, column):
        self.__columns.append(column)

    def export(self):
        data = []
        for row in self.__rows:
            row_data = {}
            for column in self.__columns:
                row_data[column] = getattr(row, column, None)
            data.append(row_data)

        with open('data/export.txt', 'w') as outfile:
            json.dump(data, outfile)

    def sort_column(self, column_name, reverse=False):
        if column_name in self.__hidden_columns:
            print('Сортировка по скрытым колонкам запрещена')
            return

        sort_values = [getattr(row, column_name, 0) for row in self.__rows]
        new_sort_values = []
        if None in sort_values:
            for value in sort_values:
                if value is None:
                    value = 0
                new_sort_values.append(value)
            sort_values = new_sort_values
        sort_values.sort(reverse=reverse)
        cash_sort_rows = []
        for i, row in enumerate(self.__rows):
            value = getattr(row, column_name, 0)
            if value is None:
                value = 0
            index = sort_values.index(value)
            row.set_sort_id(index)
            cash_sort_rows.append((row.get_sort_id(), i, row))

        cash_sort_rows.sort()
        self.__rows = [z for x, y, z in cash_sort_rows]

    def hidden_column(self, column_name):
        if column_name in self.__hidden_columns:
            self.__hidden_columns.remove(column_name)
        else:
            self.__hidden_columns.append(column_name)

    def change_position(self, column_name_first, column_name_second):
        index_change = None
        for i, column in enumerate(self.__columns):
            if column == column_name_first:
                self.__columns.pop(i)
                self.__columns.insert(i, column_name_second)
                index_change = i
        for i, column in enumerate(self.__columns):
            if column == column_name_second and index_change != i:
                self.__columns.pop(i)
                self.__columns.insert(i, column_name_first)

    def __find_row_by_id(self, row_id):
        result = None
        for row in self.__rows:
            if row_id == getattr(row, 'id', None):
                result = row

        return result

    def select_row(self, row_id):
        row = self.__find_row_by_id(row_id)
        if not row:
            print('Некорректно задан ID')

        if row in self.__selected_rows:
            self.__selected_rows.remove(row)
        else:
            self.__selected_rows.append(row)

    def delete_selected_rows(self):
        for row in self.__selected_rows:
            self.__rows.remove(row)

        self.__selected_rows = []

    def show_columns(self):
        print(self.__columns)


if __name__ == '__main__':
    with open('data/data.json', 'r') as f:
        table = Table()
        table.load_data(f.read())
        table.show_columns()
        table.change_position('country', 'alternate_name')
        table.show_columns()
        table.select_row(23)
        table.delete_selected_rows()
        table.sort_column('country')
        table.export()