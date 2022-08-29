import json
from collections import (
    defaultdict,
)

from django.apps import (
    apps,
)
from django.db import (
    connection,
)


_SLOT = 'slot'


def run_once(func):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return func(*args, **kwargs)
    wrapper.has_run = False
    return wrapper


def get_model_by_table_name(db_table):
    for model in apps.get_models():
        if model._meta.db_table == db_table:
            return model


@run_once
def start_log_db():
    """Начинает отслеживать изменения в БД."""
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT 'init' FROM pg_create_logical_replication_slot(%s, 'wal2json')",
            [_SLOT],
        )


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
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT data FROM pg_logical_slot_get_changes("
            "%s, NULL, NULL, 'pretty-print', '1', 'add-msg-prefixes', 'wal2json')",
            [_SLOT],
        )
        rows = cursor.fetchall()

    changes = defaultdict(lambda: defaultdict(int))
    for row in rows:
        row_changes = json.loads(row[0])['change']
        for change in row_changes:
            changes[change['kind'].upper()][get_model_by_table_name(change['table'])] += 1

    return changes