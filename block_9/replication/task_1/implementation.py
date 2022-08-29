from collections import (
    defaultdict,
)

import django.apps
from django.db import (
    connection,
)


SLOT_NAME = 'log_slot'

OPERATIONS = (
    'INSERT',
    'UPDATE',
    'DELETE',
)


def start_log_db():
    """Начинает отслеживать изменения в БД"""
    if run_sql(f"SELECT 1 FROM pg_replication_slots WHERE slot_name = '{SLOT_NAME}'"):
        run_sql(f"SELECT pg_drop_replication_slot('{SLOT_NAME}')")

    run_sql(f"SELECT * FROM pg_create_logical_replication_slot('{SLOT_NAME}', 'test_decoding')")


def get_db_changes_info() -> dict:
    """Возвращает информацию об изменениях в БД.

    Формат ответа:
    {
        ТипОперации: {
            Модель: Количество затронутых записей,
            Модель: Количество затронутых записей,
            ............
        },
        {
        .............
    }
    """
    result = defaultdict(lambda: defaultdict(int))
    models_by_tables = {f'public.{model._meta.db_table}': model for model in django.apps.apps.get_models()}

    for change in run_sql(f"SELECT * FROM pg_logical_slot_get_changes('{SLOT_NAME}', NULL, NULL)"):
        query = change[2]

        for operation in OPERATIONS:
            if operation in query:
                for table, model in models_by_tables.items():
                    if table in query:
                        result[operation][model] += 1

    return result


def run_sql(sql):
    with connection.cursor() as cursor:
        cursor.execute(sql)
        rows = cursor.fetchall()

    return rows
