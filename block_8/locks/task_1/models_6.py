from django.db import (
    models,
)


class Account(models.Model):

    balance = models.IntegerField(default=0)
    version = models.IntegerField(default=0)

    class Meta:
        db_table = 'locks_1_account'

    def deposit(self, amount):
        actual_account = self._get_actual_account()
        if self.version != actual_account['version']:
            self.__dict__.update(actual_account)

        self.version += 1
        self.balance += amount
        self.save()

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError('Сумма снятия больше, чем баланс счета')

        actual_account = self._get_actual_account()
        if self.version != actual_account['version']:
            self.__dict__.update(actual_account)

        self.version += 1
        self.balance -= amount
        self.save()

    def _get_actual_account(self):
        return self.__class__.objects.filter(pk=self.pk).values('balance','version').first()