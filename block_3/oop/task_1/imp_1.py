import json
import operator
from copy import copy

from os import path


class Table:
    def __init__(self):
        self._columns = None
        self._strings = []

    def _set_columns(self, data_table):
        titles = data_table[0].keys()
        data_columns = {
            title: {
                'filter': False,
                'hide': False,
                'number': number
            } for number, title in enumerate(titles)}
        self._columns = Columns(data_columns)

    def _set_strings(self, data_table):
        self._strings = [String(string) for string in data_table]

    def load_data(self, name):
        parent_dir = path.dirname(path.abspath(__file__))
        with open(path.join(parent_dir, 'data', f'{name}.json')) as f:
            data_table = json.load(f)
        self._set_columns(data_table)
        self._set_strings(data_table)
        return data_table

    def select_string(self, id):
        for string in self._strings:
            if string.get_id() == id:
                string.select()
                break

    def delete_select_string(self):
        for string in self._strings:
            if string.get_status_select():
                string.delete()

    def sort(self, title, reverse=False):
        self._columns.set_sort(title, reverse=reverse)

    def filter(self, title, value):
        self._columns.set_filter(title, value)

    def hide_column(self, title):
        self._columns.hide_column(title)

    def change_column(self, first_cloumn, second_column):
        self._columns.change_column(first_cloumn, second_column)

    def _sort(self):
        columns = self._columns
        sort = columns.get_sort()
        title = sort.get('title')
        reverse = sort.get('reverse')
        if not columns.status_hide_column(title):
            self._strings.sort(
                key=operator.attrgetter(f'{title}'),
                reverse=reverse)

    def _filter(self):
        columns = self._columns
        data = columns.get_data()
        for column_title in data:
            if (data[column_title]['filter']
                    and not columns.status_hide_column(column_title)):
                result = []
                value = data[column_title].get('filter')
                for string in self._strings:
                    if value in str(getattr(string, column_title)):
                        result.append(string)
                self._strings = result

    def _delete_select_string(self):
        result = []
        for string in self._strings:
            if not string.get_status_delete():
                result.append(string)
        self._strings = result

    def _string_processing(self):
        self._delete_select_string()
        self._filter()
        self._sort()

    def _generation_dictionary(self):
        result = []
        template = self._columns.create_template()
        for string in self._strings:
            template = copy(template)
            for title_column in template:
                template[title_column] = getattr(string, title_column)
            result.append(template)
        return result

    def _get_result_dict(self):
        self._string_processing()
        return self._generation_dictionary()

    def export(self, file_name):
        parent_dir = path.dirname(path.abspath(__file__))
        with open(
                path.join(parent_dir, 'data', f'{file_name}.json'),
                'w',
                encoding='utf-8'
        ) as f:
            json.dump(self._get_result_dict(), f, ensure_ascii=False, indent=4)


class Columns:
    def __init__(self, data_columns):
        self._sort = {'title': 'id',
                      'reverse': False}
        self._data = data_columns

    def set_sort(self, title, reverse):
        self._sort.update({'title': title,
                           'reverse': reverse})

    def get_sort(self):
        return self._sort

    def set_filter(self, title, value):
        self._data[title]['filter'] = value

    def get_data(self):
        return self._data

    def change_column(self, first_cloumn, second_column):
        self._data[first_cloumn]['number'], self._data[second_column][
            'number'] = self._data[second_column]['number'], \
                        self._data[first_cloumn]['number']

    def hide_column(self, title):
        self._data[title]['hide'] = True

    def status_hide_column(self, title):
        return self._data[title]['hide']

    def create_template(self):
        title_column_list = [None for column in self.get_data()]
        data = self.get_data()
        for title_column in self.get_data():
            column = data[title_column]
            if not column['hide']:
                title_column_list[column['number']] = title_column
        result_dict = {title_column: None for title_column in
                       title_column_list if title_column}
        return result_dict


class String:

    def __init__(self, string):
        self._status_select = False
        self._status_delete = False
        self.__dict__.update(string)

    def __repr__(self):
        return f'id = {self.id}'

    def select(self):
        self._status_select = True

    def delete(self):
        self._status_delete = True

    def get_id(self):
        return str(self.id)

    def get_status_select(self):
        return self._status_select

    def get_status_delete(self):
        return self._status_delete


table = Table()
table.load_data('data')

# Смена столбцов
table.change_column('country', 'fifa_code')

# Скрытие столбца
table.hide_column('group_letter')

# Сортировка по убыванию
table.sort('country', reverse=True)

# Фильтровка
table.filter('group_id', '5')

# Выделение строк
table.select_string('20')
table.select_string('18')

# Удаление выделенных строк
table.delete_select_string()

table.export('result')