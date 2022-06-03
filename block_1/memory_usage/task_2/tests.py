from unittest import (
    TestCase,
)

from block_1.memory_usage.task_2.implementation import (
    create_object,
)


class Test(TestCase):

    def test_object_with_usage(self):
        a = create_object('A')
        self.assertEqual(len(create_object._cache), 1)

    def test_object_without_usage(self):
        create_object('A')
        self.assertEqual(len(create_object._cache), 0)

    def test_object_with_del(self):
        a = create_object('A')
        del(a)
        self.assertEqual(len(create_object._cache), 0)