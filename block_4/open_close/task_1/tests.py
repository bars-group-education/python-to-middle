from unittest import TestCase

from block_4.open_close.task_1.implementation import CashBox, Product, CardType


class Test(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.cashbox = CashBox()

    def test_a_bronze(self):
        self.assertEqual(self.cashbox.get_total_sum(Product.A, CardType.BRONZE), 9000)

    def test_a_silver(self):
        self.assertEqual(self.cashbox.get_total_sum(Product.A, CardType.SILVER), 8500)

    def test_a_gold(self):
        self.assertEqual(self.cashbox.get_total_sum(Product.A, CardType.GOLD), 8000)

    def test_b_bronze(self):
        self.assertEqual(self.cashbox.get_total_sum(Product.B, CardType.BRONZE), 18000)

    def test_b_silver(self):
        self.assertEqual(self.cashbox.get_total_sum(Product.B, CardType.SILVER), 17000)

    def test_b_gold(self):
        self.assertEqual(self.cashbox.get_total_sum(Product.B, CardType.GOLD), 16000)

    def test_c_bronze(self):
        self.assertEqual(self.cashbox.get_total_sum(Product.C, CardType.BRONZE), 27000)

    def test_c_silver(self):
        self.assertEqual(self.cashbox.get_total_sum(Product.C, CardType.SILVER), 25500)

    def test_c_gold(self):
        self.assertEqual(self.cashbox.get_total_sum(Product.C, CardType.GOLD), 24000)
