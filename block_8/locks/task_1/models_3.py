from django.db import (
    models,
)

from django.db import transaction


class Account(models.Model):

    balance = models.IntegerField(default=0)

    class Meta:
        db_table = 'locks_1_account'

    def deposit(self, amount):
        with transaction.atomic():
            this_account = self.__class__.objects.select_for_update().get(id=self.id)
            this_account.balance += amount
            this_account.save()

    def withdraw(self, amount):
        with transaction.atomic():
            this_account = self.__class__.objects.select_for_update().get(id=self.id)
            if amount > this_account.balance:
                raise ValueError('Сумма снятия больше, чем баланс счета')

            this_account.balance -= amount
            this_account.save()