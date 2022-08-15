from django.db import (
    transaction,
)

from block_8.acid.task_1.exceptions import (
    BadConnection,
)
from block_8.acid.task_1.models import (
    Document,
    FailedDocument,
    Stack,
)


def save_stack_of_documents(stack_data):
    for stack_item in stack_data:

        with transaction.atomic():
            stack = Stack.objects.create(name=stack_item['stack']['name'])
            created = 0
            failed_docs = []

            for document in stack_item['stack']['documents']:
                try:
                    Document.objects.create(number=document['number'], stack=stack)
                except BadConnection:
                    failed_docs.append(FailedDocument(number=document['number'], stack=stack))
                else:
                    created += 1

            if created:
                FailedDocument.objects.bulk_create(failed_docs)
            else:
                transaction.set_rollback(True)