from django.db import (
    models,
)


class Account(models.Model):

    balance = models.IntegerField(default=0)

    class Meta:
        db_table = 'locks_2_account'

    def deposit(self, amount):
        self.change_amount(amount)

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError('Сумма снятия больше, чем баланс счета')

        self.change_amount(-1 * amount)

    def change_amount(self, amount):
        while True:
            account = Account.objects.get(pk=self.id)

            updated = Account.objects.filter(
                id=account.id,
                balance=account.balance
            ).update(
                balance=account.balance + amount,
                version=account.version + 1,
            )

            if updated > 0:
                break