import json
import os
from unittest import TestCase

from block_4.single_responsibility.task_1.implementation import RecordStore, Record


class Test(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.path = 'result.txt'

    def tearDown(self) -> None:
        super().tearDown()
        try:
            os.remove(self.path)
        except:
            pass

    def test(self):
        r1 = Record(1, 'Один')
        r2 = Record(2, 'два')
        r3 = Record(3, 'Три')

        store = RecordStore()
        store.add_record(r1)
        store.add_record(r2)
        store.add_record(r3)

        store.del_record(r2)

        json_result = store.to_json()
        self.assertEqual(json_result, json.dumps([{1: "Один"}, {3: "Три"}]))

        store.save_to_file(self.path)
        with open(self.path) as f:
            self.assertEqual(json.loads(f.read()), [{"1": "Один"}, {"3": "Три"}])
