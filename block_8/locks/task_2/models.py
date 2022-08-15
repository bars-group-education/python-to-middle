from django.db import (
    models, transaction,
)
from django.db.models import F


class Account(models.Model):

    balance = models.IntegerField(default=0)
    version = models.IntegerField(default=0)

    class Meta:
        db_table = 'locks_2_account'

    def deposit(self, amount):
        instance = self._get_actual_instance(self)
        instance._update_balance(amount)

    def withdraw(self, amount):
        instance = self._get_actual_instance(self)
        instance._update_balance(-amount)

    @classmethod
    def _get_actual_instance(cls, current_instance):
        return cls.objects(id=current_instance.id)

    def _update_balance(self, amount):
        instance = self

        for iteration in range(10):

            with transaction.atomic():
                updated = instance.__class__.objects.filter(
                    pk=instance.pk,
                    version=instance.version,
                ).update(
                    balance=F('balance') + amount,
                    version=instance.version + 1,
                )

                if updated:
                    if amount > instance.balance:
                        raise ValueError('Сумма снятия больше, чем баланс счета')
                    else:
                        return

            instance = self._get_actual_instance(instance)

        raise Exception




