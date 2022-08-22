from django.contrib.postgres.indexes import GinIndex, GistIndex
from django.db import (
    models,
)
from django.db.models import Index


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
        index_together = (('fname', 'iname', 'oname'), )
        indexes = [
            Index(fields=['fname', 'iname', 'oname'], name='name_index'),
            GistIndex(fields=['begin', 'end'], name='begin_end_index'),
            GinIndex(fields=['country'], name='country_index'),
            GinIndex(fields=['additional_info'], name='additional_info_gin_index')
        ]