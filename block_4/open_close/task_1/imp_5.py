from enum import Enum


class CardType(Enum):
    BRONZE = 1
    SILVER = 2
    GOLD = 3


class Product(Enum):
    A = 10000
    B = 20000
    C = 30000


class CostInterface:
    def get_cost(self):
        raise NotImplementedError


class DiscountInterface:
    def get_discount(self):
        raise NotImplementedError


class EnumProduct(CostInterface):
    def __init__(self, product):
        self._product = product

    def get_cost(self):
        return self._product.value if self._product else 0


class CardDiscount(DiscountInterface):
    discount = {
        CardType.BRONZE: 5,
        CardType.SILVER: 10,
        CardType.GOLD: 15
    }

    def __init__(self, card_type):
        self._card_type = card_type

    def get_discount(self):
        return self.discount.get(self._card_type, 0)


class CashBox:
    class_products = EnumProduct
    class_discount = CardDiscount

    _base_discount = 5

    def get_total_sum(self, product, card_type):
        cost = self.class_products(product).get_cost()
        discount = self._base_discount + self.class_discount(card_type).get_discount()

        total_sum = cost - (cost * discount / 100.0)

        return total_sum




