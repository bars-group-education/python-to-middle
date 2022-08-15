from django.db import (
    models,
)


class BaseModel(models.Model):
    text = models.CharField('Наименование', max_length=300, default='')

    class Meta:
        abstract = True


class A(BaseModel):
    """
    Модель A.
    """

    class Meta:
        db_table = 'replication_a'


class B(BaseModel):
    """
    Модель B.
    """

    class Meta:
        db_table = 'replication_b'


class C(BaseModel):
    """
    Модель C.
    """

    class Meta:
        db_table = 'replication_c'
