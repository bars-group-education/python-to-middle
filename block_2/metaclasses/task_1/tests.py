from unittest import TestCase

from block_2.metaclasses.task_1.implementation import Updateable


class Test(TestCase):

    def test_class(self):
        class DynamicClass(metaclass=Updateable):
            def foo(self):
                return 'old'

        c = DynamicClass()
        self.assertEqual(c.foo(), 'old')

        class DynamicClass(metaclass=Updateable):
            def foo(self):
                return 'new'

        self.assertEqual(c.foo(), 'new')
