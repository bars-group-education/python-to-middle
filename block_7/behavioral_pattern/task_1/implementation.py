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
    # нужно добавить свой код сюда


class PlusOperation(ArithmeticOperation):
    """Операция сложения"""
    # нужно добавить свой код сюда


class DevideOperation(ArithmeticOperation):
    """Операция деления"""
    # нужно добавить свой код сюда


class MultiplyOperation(ArithmeticOperation):
    """Опрация умножения"""
    # нужно добавить свой код сюда
