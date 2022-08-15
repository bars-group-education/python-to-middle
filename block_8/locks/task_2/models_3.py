from django.db import (
    models,
)

from block_8.locks.task_2.exceptions import WrongBalanceVersion


class Account(models.Model):

    balance = models.IntegerField(default=0)
    version = models.IntegerField(default=0)

    class Meta:
        db_table = 'locks_2_account'

    def deposit(self, amount):
        self.balance += amount

        try:
            self.save()
        except WrongBalanceVersion:
            # Получим актуальные данные и выполним операцию
            actual_account = self._get_actual_account()
            actual_account['balance'] += amount
            self.__dict__.update(actual_account)

            self.save()

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError('Сумма снятия больше, чем баланс счета')

        self.balance -= amount

        try:
            self.save()
        except WrongBalanceVersion:
            # Получим актуальные данные и выполним операцию
            actual_account = self._get_actual_account()
            actual_account['balance'] -= amount
            self.__dict__.update(actual_account)

            self.save()

    def _get_actual_account(self):
        return self.__class__.objects.filter(pk=self.pk).values('balance','version').first()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        if self.pk:
            rows = self.__class__.objects.filter(
                pk=self.pk,
                version=self.version,
            ).update(
                balance=self.balance,
                version=self.version + 1,
            )
            if not rows:
                raise WrongBalanceVersion

            self.version += 1

        super().save(force_insert, force_update, using, update_fields)