# Generated by Django 3.2.13 on 2022-08-08 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='A',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(default='', max_length=300, verbose_name='Наименование')),
            ],
            options={
                'db_table': 'replication_a',
            },
        ),
        migrations.CreateModel(
            name='B',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(default='', max_length=300, verbose_name='Наименование')),
            ],
            options={
                'db_table': 'replication_b',
            },
        ),
        migrations.CreateModel(
            name='C',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(default='', max_length=300, verbose_name='Наименование')),
            ],
            options={
                'db_table': 'replication_c',
            },
        ),
    ]
