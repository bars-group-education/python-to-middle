from enum import Enum


class CardType(Enum):
    BRONZE = 1
    SILVER = 2
    GOLD = 3


DISCOUNT_MAP = {
    CardType.BRONZE: 5,
    CardType.SILVER: 10,
    CardType.GOLD: 15,
}


class Product(Enum):
    A = 10000
    B = 20000
    C = 30000


class CashBox:

    def get_product_cost(self, product):
        if not isinstance(product, Product):
            raise TypeError
        return Product[product.name].value

    def get_discount(self, card_type, default=5):
        if not isinstance(card_type, CardType):
            raise TypeError
        return default + DISCOUNT_MAP[card_type]

    def get_total_sum(self, product, card_type):
        cost = self.get_product_cost(product)
        discount = self.get_discount(card_type)
        total_sum = cost - (cost * discount / 100.0)

        return total_sum