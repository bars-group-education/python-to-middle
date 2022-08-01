import operator
import re
from abc import abstractmethod


_OPERATION_MAP = {
    '*': operator.mul,
    '-': operator.sub,
    '+': operator.add,
    '/': operator.truediv,
}


class ArithmeticOperation:

    def __init__(self, handler=None):
        """Инициализация класса.

        :param handler: следующий обработчик в цепочке
        """
        self._next_handler = handler

    @abstractmethod
    def calculate(self, operation: str) -> int:
        """Расчет результата вычислительной операции.

        :param operation: операция записанная в виде строки
        :return: целочисленный результат
        """
        if self._next_handler:
            return self._next_handler.calculate(operation)

        return None

    def get_operands(self, operation) -> tuple[int, int]:
        operands = re.findall(r'\d+', operation)
        if len(operands) != 2:
            raise ValueError('Неверно заданы операнды')

        return int(operands[0]), int(operands[1])

class MinusOperation(ArithmeticOperation):
    """Операция вычитания."""

    def calculate(self, operation: str):
        if '-' in operation:
            return _OPERATION_MAP['-'](*self.get_operands(operation))
        else:
            return super().calculate(operation)

class PlusOperation(ArithmeticOperation):
    """Операция сложения."""

    def calculate(self, operation: str):
        if '+' in operation:
            return _OPERATION_MAP['+'](*self.get_operands(operation))
        else:
            return super().calculate(operation)


class DevideOperation(ArithmeticOperation):
    """Операция деления."""

    def calculate(self, operation: str):
        if '/' in operation:
            return _OPERATION_MAP['/'](*self.get_operands(operation))
        else:
            return super().calculate(operation)


class MultiplyOperation(ArithmeticOperation):
    """Опрация умножения."""

    def calculate(self, operation: str):
        if '*' in operation:
            return _OPERATION_MAP['*'](*self.get_operands(operation))
        else:
            return super().calculate(operation)