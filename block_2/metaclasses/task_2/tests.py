import io
import sys

from unittest import TestCase

from block_2.metaclasses.task_2.implementation import Lazy


class Test(TestCase):

    def test_function(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output

        def return_3():
            print('create')

            return 3

        number = Lazy(return_3)
        first_result = number + 2

        self.assertEqual(captured_output.getvalue(), 'create\n')
        self.assertEqual(first_result, 5)

        second_result = number + 2

        self.assertEqual(captured_output.getvalue(), 'create\n')
        self.assertEqual(second_result, 5)

    def test_lambda(self):
        lazy_list = Lazy(lambda: [])
        self.assertEqual(lazy_list, [])

        lazy_list.append('item')
        self.assertEqual(lazy_list, ['item'])

        self.assertIs(type(lazy_list), Lazy)

    def test_instance(self):
        class A:
            pass

        instance = Lazy(lambda: A())
        self.assertIs(type(instance), Lazy)

        instance.a = 0
        self.assertEqual(instance.a, 0)

        with self.assertRaises(AttributeError):
            instance.b

        with self.assertRaises(TypeError):
            instance + 1
