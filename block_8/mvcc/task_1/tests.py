from django.test import (
    TransactionTestCase
)

from block_8.mvcc.task_1.models import Customer


class MyTestCase(TransactionTestCase):

    def test_save(self):
        customer = Customer()
        customer.fix_reg_date()
        customer.change_name('Customer')
        customer.change_name('Customer')
        customer.change_name('Customer')
        customer.change_name('Customer')
        customer.change_email('blasblasd@dasdasd.ru')
        customer.save()
        self.assertEqual(customer._count_save, 1)