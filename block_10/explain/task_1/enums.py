from django.db import models


class Location(models.TextChoices):
    IN = '1', 'В библиотеке'
    OUT = '2', 'Вне библиотеки'