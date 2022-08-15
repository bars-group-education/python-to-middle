from django.db import (
    transaction,
)
from django.test import (
    TransactionTestCase,
)

from block_9.replication.task_1.implementation import (
    get_db_changes_info, start_log_db,
)
from block_9.replication.task_1.models import (
    A,
    B,
    C,
)


class MyTestCase(TransactionTestCase):

    def test_insert(self):
        start_log_db()

        for i in range(10):
            A.objects.create()

        for i in range(20):
            C.objects.create()

        changes = get_db_changes_info()

        self.assertEqual(changes['INSERT'][A], 10)
        self.assertEqual(changes['INSERT'][C], 20)

    def test_update(self):
        start_log_db()

        for i in range(10):
            A.objects.create()

        for item in A.objects.all()[:5]:
            item.text = 'text'
            item.save()

        changes = get_db_changes_info()

        self.assertEqual(changes['INSERT'][A], 10)
        self.assertEqual(changes['UPDATE'][A], 5)

    def test_delete(self):
        start_log_db()

        for i in range(10):
            B.objects.create()

        for item in B.objects.all()[:5]:
            item.delete()

        changes = get_db_changes_info()

        self.assertEqual(changes['INSERT'][B], 10)
        self.assertEqual(changes['DELETE'][B], 5)

    def test_rollback(self):
        start_log_db()

        with transaction.atomic():
            for i in range(10):
                C.objects.create()

            for item in C.objects.all()[:5]:
                item.text = 'text'
                item.save()

            for item in C.objects.all()[:5]:
                item.delete()

        changes = get_db_changes_info()

        self.assertEqual(changes, {})
