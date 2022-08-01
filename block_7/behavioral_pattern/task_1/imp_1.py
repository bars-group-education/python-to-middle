from abc import abstractmethod
import operator


def calc(operand, operation):
    operands = {
        '+': operator.add,
        '-': operator.sub,
        '/': operator.truediv,
        '*': operator.mul,
    }
    if operand in operation:
        numbers = operation.split(operand)
        return operands[operand](int(numbers[0]), int(numbers[1]))


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


class MinusOperation(ArithmeticOperation):
    """Операция вычитания"""

    def calculate(self, operation: str) -> int:
        if res := calc('-', operation):
            return res
        elif self._next_handler:
            return self._next_handler.calculate(operation)


class PlusOperation(ArithmeticOperation):
    """Операция сложения"""

    def calculate(self, operation: str) -> int:
        if res := calc('+', operation):
            return res
        elif self._next_handler:
            return self._next_handler.calculate(operation)


class DevideOperation(ArithmeticOperation):
    """Операция деления"""

    def calculate(self, operation: str) -> int:
        if res := calc('/', operation):
            return res
        elif self._next_handler:
            return self._next_handler.calculate(operation)


class MultiplyOperation(ArithmeticOperation):
    """Опрация умножения"""

    def calculate(self, operation: str) -> int:
        if res := calc('*', operation):
            return res
        elif self._next_handler:
            return self._next_handler.calculate(operation)