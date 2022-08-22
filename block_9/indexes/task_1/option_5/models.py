from django.contrib.postgres.indexes import GinIndex, OpClass
from django.db import (
    models,
)
from django.db.models.functions import Upper


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
            models.Index(fields=['fname', 'iname', 'oname']),
            models.Index(fields=['country']),
            models.Index(fields=['begin']),
            models.Index(fields=['end']),
            # Индексы для полнотекстового поиска
            models.Index(Upper('additional_info'), name='additional_info_upper_index'),
            GinIndex(
                OpClass(Upper('additional_info'), name='gin_trgm_ops'),
                name='additional_info_gin_idx',
            ),
        ]