from django.db import (
    models,
)

from django.contrib.postgres.operations import BtreeGinExtension

from django.contrib.postgres.indexes import GinIndex, GistIndex


class Employee(models.Model):
    """Сотрудник."""

    inn = models.CharField('ИНН', max_length=12)
    fname = models.CharField('Фамилия', max_length=300, db_index=True)
    iname = models.CharField('Имя', max_length=300, db_index=True)
    oname = models.CharField('Отчество', max_length=300, null=True, db_index=True)
    country = models.CharField('Страна местонахождения на момент приема', max_length=3, db_index=True)
    department_id = models.IntegerField('ID подразделения')
    position_id = models.IntegerField('ID должности')
    begin = models.DateField('Дата приема', db_index=True)
    end = models.DateField('Дата увольнения', null=True, db_index=True)
    additional_info = models.TextField('Дополнительная информация', default='', db_index=True)

    class Meta:
        db_table = 'indexes_employees'
        indexes = [
            models.Index(fields=['fname', 'iname', 'oname']),
            GinIndex(fields=['country']),
            GistIndex(fields=['begin', 'end']),

            GinIndex(fields=['additional_info'], name='additional_info_gin_index', opclasses=['gin_trgm_ops'])
        ]