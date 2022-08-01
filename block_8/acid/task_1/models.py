from django.db import (
    models,
)


class Stack(models.Model):
    """Пачка документов."""

    name = models.CharField('Наименование', max_length=300)

    class Meta:
        db_table = 'acid_stack'


class BaseDocument(models.Model):
    """Базовый документ."""

    stack = models.ForeignKey('Stack', on_delete=models.CASCADE, verbose_name='Пачка')
    number = models.CharField('Номер', max_length=10)


class Document(BaseDocument):
    """Документ."""

    valid = models.BooleanField(verbose_name='Признак валидности', default=False)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.valid = True
        self.bad_connection_emulation()

        super().save(force_insert, force_update, using, update_fields)

    def bad_connection_emulation(self):
        from block_8.acid.task_1.helpers import (
            emulator,
        )
        emulator.test()

    class Meta:
        db_table = 'acid_document'


class FailedDocument(BaseDocument):
    """Ошибочный документ."""

    class Meta:
        db_table = 'acid_failed_document'
