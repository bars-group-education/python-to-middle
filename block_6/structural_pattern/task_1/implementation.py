from abc import ABC, abstractmethod


class Visa:
    """Интерфейс платежной системы Visa"""

    def __init__(self, user_id, start_balance):
        """
            Инициализация класса
        :param user_id: Идентификатор пользователя
        :param start_balance: Стартовый баланс
        """
        self.user_id = user_id
        self.current_balance = start_balance

    def transfer_money(self, amount):
        """
            Перевод денег из системы
        :param amount: количество денег для перевода
        """
        self.current_balance -= amount

    def receive_money(self, amount):
        """
            Поревод денег в систему
        :param amount: количество денег для перевода
        """
        self.current_balance += amount

    @property
    def balance(self):
        """Текущий баланс"""
        return self.current_balance


class MasterCard:
    """Интерфейс платежной системы MasterCard"""

    def __init__(self, inn, money):
        """
            Инициализация класса
        :param inn: ИНН пользователя
        :param money: Начальное количество денег на счету
        """
        self.user_inn = inn
        self.money = money

    def take(self, quantity):
        """
            Извлечение денег из системы
        :param quantity: количество извлеченных денег
        """
        self.money -= quantity

    def put(self, quantity):
        """
            Перемещение денег в систему
        :param quantity: количество перемещенных денег
        """
        self.money += quantity

    def current_money(self):
        """
            Запрос текущего количества денег на счете
        :return: количество денег на счете
        """
        return self.money


class PaymentAdapter(ABC):

    def __init__(self, payment_system):
        """
            Инициализация класса
        :param payment_system: платежная система
        """
        self.payment_system = payment_system

    @abstractmethod
    def send(self, money):
        """
            Снятие деньг со счета
        :param money: количество денег для снятия
        """
        pass

    @abstractmethod
    def receive(self, money):
        """
            Получение денег на счет
        :param money: количество денег для получения
        """
        pass

    @property
    @abstractmethod
    def money(self):
        """Получение текущего баланса"""
        pass


class VisaPaymentAdapter(PaymentAdapter):
    """Адаптер платежной системы Visa"""
    # нужно добавить свой код сюда


class MasterCardPaymentAdapter(PaymentAdapter):
    """Адаптер платежной системы MasterCard"""
    # нужно добавить свой код сюда

