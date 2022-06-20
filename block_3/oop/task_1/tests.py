import json
from unittest import TestCase

from block_3.oop.task_1.implementation import Table


class Test(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.table = Table()
        with open('data/data.json', 'r') as f:
            self.table.load_data(f.read())

    def test_plain(self):
        result = self.table.export()
        with open('data/test_plain.json', 'r') as f:
            self.assertEqual(result, json.loads(f.read()))
