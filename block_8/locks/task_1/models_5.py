from django.db import (
    models, transaction,
)
from django.db.models import F


class Account(models.Model):
    balance = models.IntegerField(default=0)

    class Meta:
        db_table = 'locks_1_account'

    def deposit(self, amount):
        Account.objects.filter(
            pk=self.pk
        ).update(
            balance=F('balance') + amount
        )

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError('Сумма снятия больше, чем баланс счета')

        Account.objects.filter(
            pk=self.pk
        ).update(
            balance=F('balance') - amount
        )