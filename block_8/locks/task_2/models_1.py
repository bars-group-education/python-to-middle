from django.db import (
    models,
)


class Account(models.Model):

    balance = models.IntegerField(default=0)
    version = models.IntegerField(default=0)

    class Meta:
        db_table = 'locks_2_account'

    def deposit(self, amount):
        Account.objects.filter(id=self.id, version=models.F('version')).update(
            balance=models.F('balance') + amount,
            version=models.F('version') + 1,
        )

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError('Сумма снятия больше, чем баланс счета')

        Account.objects.filter(id=self.id, version=models.F('version')).update(
            balance=models.F('balance') - amount,
            version=models.F('version') + 1,
        )