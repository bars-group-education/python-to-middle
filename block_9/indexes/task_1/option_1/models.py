from django.db import (
    models,
)
from django.contrib.postgres.indexes import GinIndex, OpClass, HashIndex
from django.db.models import Value, CharField
from django.db.models.expressions import RawSQL
from django.db.models.functions import Upper, Concat


class Employee(models.Model):
    """Сотрудник."""

    inn = models.CharField('ИНН', max_length=12)
    fname = models.CharField('Фамилия', max_length=300)
    iname = models.CharField('Имя', max_length=300)
    oname = models.CharField('Отчество', max_length=300, null=True)
    country = models.CharField('Страна местонахождения на момент приема', max_length=3)
    department_id = models.IntegerField('ID подразделения')
    position_id = models.IntegerField('ID должности')
    begin = models.DateField('Дата приема')
    end = models.DateField('Дата увольнения', null=True)
    additional_info = models.TextField('Дополнительная информация', default='')

    class Meta:
        db_table = 'indexes_employees'
        indexes = [
            # period
            models.Index(fields=['begin']),
            models.Index(fields=['end']),

            # country
            models.Index(fields=['country']),

            # additional_info
            GinIndex(
                fields=['additional_info'],
                opclasses=['gin_trgm_ops'],
                name='additional_info_idx',
            ),
            GinIndex(
                OpClass(Upper('additional_info'), name='gin_trgm_ops'),
                name='additional_info_upper_idx'
            ),
        ]