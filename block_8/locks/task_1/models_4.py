from django.db import (
    models, transaction,
)


class Account(models.Model):

    balance = models.IntegerField(default=0)

    class Meta:
        db_table = 'locks_1_account'

    def deposit(self, amount):
        self.change_amount(self.id, amount)

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError('Сумма снятия больше, чем баланс счета')

        self.change_amount(self.id, -1 * amount)

    @classmethod
    def change_amount(cls, _id, amount):
        with transaction.atomic():
            account = cls.objects.select_for_update().get(pk=_id)
            account.balance += amount
            account.save()