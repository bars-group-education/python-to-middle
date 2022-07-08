import unittest

from block_6.structural_pattern.task_1.implementation import Visa, MasterCard, VisaPaymentAdapter, \
    MasterCardPaymentAdapter


class MyTestCase(unittest.TestCase):

    def test_visa_to_mastercard(self):
        visa = Visa('63dw4523', 100)
        master_card = MasterCard('119367144330', 7)
        visa_adapter = VisaPaymentAdapter(visa)
        master_card_adapter = MasterCardPaymentAdapter(master_card)
        visa_adapter.send(45)
        master_card_adapter.receive(45)

        self.assertEqual(visa_adapter.money, 55)
        self.assertEqual(master_card_adapter.money, 52)

    def test_mastercard_to_visa(self):
        visa = Visa('63dw4523', 11)
        master_card = MasterCard('119367144330', 88)
        visa_adapter = VisaPaymentAdapter(visa)
        master_card_adapter = MasterCardPaymentAdapter(master_card)
        master_card_adapter.send(37)
        visa_adapter.receive(37)

        self.assertEqual(visa_adapter.money, 48)
        self.assertEqual(master_card_adapter.money, 51)


if __name__ == '__main__':
    unittest.main()
