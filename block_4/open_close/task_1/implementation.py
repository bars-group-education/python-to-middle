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

    def get_total_sum(self, product, card_type):
        if product == Product.A:
            cost = Product.A.value
        elif product == Product.B:
            cost = Product.B.value
        elif product == Product.C:
            cost = Product.C.value
        else:
            cost = 0

        discount = 5

        if card_type == CardType.BRONZE:
            discount += 5

        elif card_type == CardType.SILVER:
            discount += 10

        elif card_type == CardType.GOLD:
            discount += 15

        total_sum = cost - (cost * discount / 100.0)

        return total_sum





