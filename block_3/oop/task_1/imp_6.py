import json
from prettytable import PrettyTable


class Table:
    def __init__(self):
        self.title_map = ('alternate_name', 'country', 'fifa_code', 'group_id', 'group_letter', 'id')
        self.columns = [
            {'title': 'alternate_name', 'hidden': False, 'items': []},
            {'title': 'country', 'hidden': False, 'items': []},
            {'title': 'fifa_code', 'hidden': False, 'items': []},
            {'title': 'group_id', 'hidden': False, 'items': []},
            {'title': 'group_letter', 'hidden': False, 'items': []},
            {'title': 'id', 'hidden': False, 'items': []},
        ]
        self.sort_by = ('id', False)
        # Фильтры которые должны быть применены для таблицы
        self._filter = None
        # Список id последних выбранных строк
        self._selected = []
        # Последний выведенный результат, для случая когда мы хотим выбрать строки
        self.last_result = []
        # Временное хранилище в котором будут хранится отсортированные и отфильтрованные строки
        self.tmp_store = []
        # Основное хранилище в котором хранятся базовое состояние таблицы
        self.store = []

    def load_data(self, data):
        loaded_data = json.loads(data)

        for item in loaded_data:
            row = []

            for value in item.values():
                row.append(value)

            self.store.append(row)

    def export(self):
        data = []

        for row in self.store:
            item = {}

            for index, value in enumerate(row):
                title = self.title_map[index]
                item[title] = value

            data.append(item)

        return data

    def change_column_place(self, column_title, place):
        """Устанавливает колонку в нужное место"""

        idx = self._get_column_idx_by_title(column_title)
        column = self.columns.pop(idx)
        self.columns.insert(place, column)

    def hide_column(self, column_title, hidden=False):
        """Устанавливает скрытость колонки"""

        idx = self._get_column_idx_by_title(column_title)
        self.columns[idx]['hidden'] = hidden

        if column_title in self.sort_by:
            self.set_sort('id')
            self.tmp_store = self.store

        if self._filter and column_title in self._filter:
            self.remove_filter()
            self.tmp_store = self.store

    def _get_column_idx_by_title(self, column_title):
        """Возвращает индекс колонки по заголовку"""

        for idx, column in enumerate(self.columns):
            if column.get('title') == column_title:
                return idx

    def _get_column_by_title(self, column_title):
        """Возвращает колонку по заголовку"""

        idx = self._get_column_idx_by_title(column_title)
        return self.columns[idx]

    def _do_sort(self, column_title, reverse):
        """Производит сортировки по заголовку колонки"""

        column = self._get_column_by_title(column_title)

        if not column['hidden']:
            title_idx = self.title_map.index(column_title)

            self.tmp_store = sorted(
                self.tmp_store or self.store,
                key=lambda item: item[title_idx],
                reverse=reverse,
            )

    def _do_filter(self, column_title, filter_by):
        """Производит фильтрацию по заголовку колонки"""

        column = self._get_column_by_title(column_title)

        if not column['hidden']:
            title_idx = self.title_map.index(column_title)

            self.tmp_store = list(filter(
                lambda item: item[title_idx] == filter_by,
                self.tmp_store or self.store,
            ))

    def set_filter(self, column_title, filter_by):
        """Устанавливает фильтр по колонке"""

        if column_title not in self.title_map:
            raise Exception('Такая колонка отсутствует')

        column = self._get_column_by_title(column_title)
        if not column['hidden']:
            self._filter = (column_title, filter_by)

    def set_sort(self, column_title, reverse=False):
        """Устанавливает сортировку по указанной колонке"""

        if column_title not in self.title_map:
            raise Exception('Такая колонка отсутствует')

        column = self._get_column_by_title(column_title)
        if not column['hidden']:
            self.sort_by = (column_title, reverse)

    def remove_filter(self):
        """Снимает фильтрацию"""

        self._filter = None

    def select_row(self, row_number):
        """Выбрать указанную строку из последнего отображения"""

        return self.select_rows(row_number, row_number)

    def select_rows(self, row_from, row_to):
        """Выбрать указанные строки из последнего отображения"""

        self.unselect_all_rows()
        rows = self.last_result[row_from:row_to + 1]
        id_idx = self._get_column_idx_by_title('id')
        ids = [row[id_idx] for row in rows]
        self._selected.extend(ids)

    def unselect_all_rows(self):
        """Снимает выделение всех строк"""

        self._selected.clear()

    def delete_selected_rows(self):
        """Удаляет выделенные строки"""

        id_idx = self.title_map.index('id')

        for id_ in self._selected:
            self._delete_row_from_store(id_, id_idx, self.store)
            self._delete_row_from_store(id_, id_idx, self.tmp_store)

        self.unselect_all_rows()

    def print_table(self):
        """Распечатывает таблицу применяя сортировку и фильтрацию"""

        self._do_sort(*self.sort_by)
        if self._filter:
            self._do_filter(*self._filter)

        columns_data_list = list(zip(*self.tmp_store))
        title_columns_map = list(zip(self.title_map, columns_data_list))

        for title, column_data in title_columns_map:
            column = self._get_column_by_title(title)
            column['items'][:] = column_data

        tmp_result = []
        for column in self.columns:
            if not column['hidden']:
                tmp_result.append(column['items'])

        result = list(zip(*tmp_result))
        self.last_result = result

        pretty_table = PrettyTable()
        pretty_table.field_names = [column['title'] for column in self.columns if not column['hidden']]
        pretty_table.add_rows(result)
        print(pretty_table)

        for column in self.columns:
            column['items'].clear()

    @staticmethod
    def _delete_row_from_store(id_, id_idx, store):
        """Удаляет строку из указанного стора"""

        for row in store:
            if row[id_idx] == id_:
                store.remove(row)
                break


# ТЕСТЫ

table = Table()
with open('data/data.json', 'r') as f:
    table.load_data(f.read())

table.change_column_place('country', 0)
table.change_column_place('country', 6)
table.print_table()


table.set_sort('country', reverse=True)
table.print_table()


table.set_filter('country', 'USA')
table.print_table()


table.hide_column('country', True)
table.change_column_place('country', 0)

table.set_filter('country', 'Netherlands')
table.hide_column('country', False)
table.print_table()


table.set_filter('group_letter', 'B')
table.set_sort('fifa_code')
table.print_table()


table.select_rows(0, 3)
table.delete_selected_rows()
table.print_table()


table.hide_column('country', False)
table.print_table()


table.set_filter('group_letter', 'C')
table.print_table()


table.set_sort('id')
table.print_table()
