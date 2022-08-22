from django.contrib.postgres.indexes import (
    GinIndex,
)
from django.db import (
    models,
)


class UpperGinIndex(GinIndex):

    def create_sql(self, model, schema_editor, using='', **kwargs):
        statement = super().create_sql(
            model, schema_editor, using, **kwargs
        )
        quote_name = statement.parts['columns'].quote_name

        def upper_quoted(column):
            return 'UPPER({0})'.format(quote_name(column))

        statement.parts['columns'].quote_name = upper_quoted
        return statement


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
            UpperGinIndex(
                fields=['additional_info'],
                name='additional_info_gin_index',
                opclasses=['gin_trgm_ops']
            ),
            models.Index(fields=['begin']),
            models.Index(fields=['end']),
        ]