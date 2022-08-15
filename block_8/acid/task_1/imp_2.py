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


@transaction.atomic
def save_stack_of_documents(stack_data):
    for stack_item in stack_data:
        stack = Stack.objects.create(name=stack_item['stack']['name'])

        for document in stack_item['stack']['documents']:
            try:
                Document.objects.create(number=document['number'], stack=stack)
            except BadConnection:
                FailedDocument.objects.create(number=document['number'], stack=stack)

        if stack.basedocument_set.filter(document__valid=True).count() < 1:
            transaction.set_rollback(True)