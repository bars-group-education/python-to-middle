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


class MinusOperation(ArithmeticOperation):
    """Операция вычитания"""

    operation_symbol = '-'

    def calculate(self, operation: str) -> int:
        if self.operation_symbol in operation:
            return (lambda a, b: a - b)(
                *map(int, operation.split(self.operation_symbol)))
        else:
            return self._next_handler.calculate(operation)


class PlusOperation(ArithmeticOperation):
    """Операция сложения"""

    operation_symbol = '+'

    def calculate(self, operation: str) -> int:
        if self.operation_symbol in operation:
            return (lambda a, b: a + b)(
                *map(int, operation.split(self.operation_symbol)))
        else:
            return self._next_handler.calculate(operation)


class DevideOperation(ArithmeticOperation):
    """Операция деления"""

    operation_symbol = '/'

    def calculate(self, operation: str) -> int:
        if self.operation_symbol in operation:
            return (lambda a, b: a / b)(
                *map(int, operation.split(self.operation_symbol)))
        else:
            return self._next_handler.calculate(operation)


class MultiplyOperation(ArithmeticOperation):
    """Опрация умножения"""

    operation_symbol = '*'

    def calculate(self, operation: str) -> int:
        if self.operation_symbol in operation:
            return (lambda a, b: a * b)(
                *map(int, operation.split(self.operation_symbol)))
        else:
            return self._next_handler.calculate(operation)