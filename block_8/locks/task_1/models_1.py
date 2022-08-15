from django.db import (
    models, transaction,
)


class Account(models.Model):

    balance = models.IntegerField(default=0)

    class Meta:
        db_table = 'locks_1_account'

    def _get_valid_acc(self):
        return Account.objects.get(id=self.id)

    @transaction.atomic
    def deposit(self, amount):
        valid_acc = self._get_valid_acc()
        valid_acc.balance += amount
        valid_acc.save()

    @transaction.atomic
    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError('Сумма снятия больше, чем баланс счета')

        valid_acc = self._get_valid_acc()
        valid_acc.balance -= amount
        valid_acc.save()