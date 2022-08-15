from django.db import (
    models,
    transaction,
)


class Account(models.Model):

    balance = models.IntegerField(default=0)

    class Meta:
        db_table = 'locks_1_account'

    @transaction.atomic
    def deposit(self, amount):
        account = Account.objects.select_for_update().get(id=self.id)

        account.balance += amount
        account.save()

    @transaction.atomic
    def withdraw(self, amount):
        account = Account.objects.select_for_update().get(id=self.id)

        if amount > account.balance:
            raise ValueError('Сумма снятия больше, чем баланс счета')

        account.balance -= amount
        account.save()