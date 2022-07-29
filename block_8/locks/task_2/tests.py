from django.test import (
    TransactionTestCase
)

from block_8.locks.task_2.models import Account


class MyTestCase(TransactionTestCase):

    def test_save(self):
        account = Account()
        account.balance = 100
        account.save()

        account_1 = Account.objects.get(pk=account.pk)
        account_2 = Account.objects.get(pk=account.pk)

        account_1.withdraw(30)
        account_2.deposit(50)

        result_account = Account.objects.get(pk=account.pk)
        self.assertEqual(result_account.balance, 120)