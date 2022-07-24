import unittest

from block_7.behavioral_pattern.task_1.implementation import MultiplyOperation, DevideOperation, MinusOperation, \
    PlusOperation


class MyTestCase(unittest.TestCase):

    def _make_chain(self):
        """
            Создаем цепочку обработчиков
        :return: цепочка обработчиков
        """
        multiply_handler = MultiplyOperation()
        devide_handler = DevideOperation(multiply_handler)
        minus_handler = MinusOperation(devide_handler)
        plus_handler = PlusOperation(minus_handler)

        return plus_handler

    def test_multiply(self):

        chain = self._make_chain()
        result = chain.calculate("3*5")

        self.assertEqual(result, 15)

    def test_devide(self):

        chain = self._make_chain()
        result = chain.calculate("21/7")

        self.assertEqual(result, 3)

    def test_minus(self):

        chain = self._make_chain()
        result = chain.calculate("20-30")

        self.assertEqual(result, -10)

    def test_plus(self):

        chain = self._make_chain()
        result = chain.calculate("10+12")

        self.assertEqual(result, 22)


if __name__ == '__main__':
    unittest.main()
