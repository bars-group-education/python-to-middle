from enum import Enum


class CardType(Enum):
    BRONZE = 1
    SILVER = 2
    GOLD = 3


class Product(Enum):
    A = 10000
    B = 20000
    C = 30000


class CashBox:
    def __init__(self):
        self.products = Product
        self.card_types = CardType
        self.discount = 5
        self.base_cost = 0

    def get_total_sum(self, product, card_type):
        cost = product.value if product in self.products else self.base_cost

        if card_type in self.card_types:
            self.discount += card_type.value * self.discount

        total_sum = cost - (cost * self.discount / 100.0)

        return total_sum




