from datetime import (
    date,
)

from django.db import (
    models,
)


class Customer(models.Model):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._count_save = 0

    registration_date = models.DateField(verbose_name='Дата регистрации')
    name = models.CharField(verbose_name='Имя', max_length=100)
    rating = models.IntegerField(verbose_name='Рейтинг', default=0)
    change_email = models.TextField(verbose_name='Email', default='')

    class Meta:
        db_table = 'mvcc_customer'

    def fix_reg_date(self):
        self.registration_date = date.today()
        self.save()

    def change_rating(self, new_rating):
        if new_rating < 0:
            raise ValueError('Рейтинг не может быть нижен 0')

        self.rating = new_rating
        self.save()

    def change_name(self, new_name):
        self.name = new_name
        self.save()

    def change_email(self, new_email):
        if '@' not in new_email:
            raise ValueError('Email должен содержать знак @')

        self.email = new_email
        self.save()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        self._count_save += 1
