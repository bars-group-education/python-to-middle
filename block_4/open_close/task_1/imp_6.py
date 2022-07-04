from enum import Enum


class CardType(Enum):
    BRONZE = 1
    SILVER = 2
    GOLD = 3

    def get_discont(self):
        return 5 + self.value * 5


class Product(Enum):
    A = 10000
    B = 20000
    C = 30000

    def get_cost(self):
        return self.value


class CashBox:

    def get_total_sum(self, product, card_type):

        cost = product.get_cost()
        discount = card_type.get_discont()

        total_sum = cost - (cost * discount / 100.0)

        return total_sum
