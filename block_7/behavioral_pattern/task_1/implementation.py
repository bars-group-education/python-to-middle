from abc import abstractmethod


class ArithmeticOperation:

    def __init__(self, handler=None):
        """
            Инициализация класса
        :param handler: следующий обработчик в цепочке
        """
        self._next_handler = handler

    @abstractmethod
    def calculate(self, operation: str) -> int:
        """
            Расчет результата вычислительной операции
            :param operation: операция записанная в виде строки
            :return: целочисленный результат
        """
        pass


class SimpleArithmeticOperation(ArithmeticOperation):

    sign = None

    def calculate(self, operation: str) -> int:
        if self.sign in operation:
            result = eval(operation)
        elif self._next_handler:
            result = self._next_handler.calculate(operation)
        else:
            raise ValueError

        return result


class MinusOperation(SimpleArithmeticOperation):
    """Операция вычитания"""
    # нужно добавить свой код сюда

    sign = '-'


class PlusOperation(SimpleArithmeticOperation):
    """Операция сложения"""
    # нужно добавить свой код сюда

    sign = '+'


class DevideOperation(SimpleArithmeticOperation):
    """Операция деления"""
    # нужно добавить свой код сюда

    sign = '/'


class MultiplyOperation(SimpleArithmeticOperation):
    """Опрация умножения"""
    # нужно добавить свой код сюда

    sign = '*'
