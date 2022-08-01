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
    def calculate(self, operation) -> int:
        if '-' in operation:
            first_num, second_num = (int(operation.split('-')[0]), int(operation.split('-')[1]))
            return first_num - second_num
        elif self._next_handler is not None:
            return self._next_handler.calculate(operation)


class PlusOperation(ArithmeticOperation):
    """Операция сложения"""
    # нужно добавить свой код сюда
    def calculate(self, operation):
        if '+' in operation:
            first_num, second_num = (int(operation.split('+')[0]), int(operation.split('+')[1]))
            return first_num + second_num
        elif self._next_handler is not None:
            return self._next_handler.calculate(operation)


class DevideOperation(ArithmeticOperation):
    """Операция деления"""
    # нужно добавить свой код сюда
    def calculate(self, operation):
        if '/' in operation:
            first_num, second_num = (int(operation.split('/')[0]), int(operation.split('/')[1]))
            return first_num / second_num
        elif self._next_handler is not None:
            return self._next_handler.calculate(operation)


class MultiplyOperation(ArithmeticOperation):
    """Опрация умножения"""
    # нужно добавить свой код сюда
    def calculate(self, operation):
        if '*' in operation:
            first_num, second_num = (int(operation.split('*')[0]), int(operation.split('*')[1]))
            return first_num * second_num
        elif self._next_handler is not None:
            return self._next_handler.calculate(operation)
