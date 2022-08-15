from typing import Dict, Union, List

from django.db import transaction, IntegrityError

from block_8.acid.task_1.exceptions import BadConnection
from block_8.acid.task_1.models import Stack, Document, FailedDocument, \
    BaseDocument


def save_stack_of_documents(
    stack_data: List[Dict[str, Dict[str, Union[str, List[Dict[str, str]]]]]]
):
    for data in stack_data:
        sid = transaction.savepoint()

        bad_documents = []

        stack_name = data['stack']['name']
        stack_documents = data['stack']['documents']

        stack = Stack.objects.create(name=stack_name)

        for document in stack_documents:
            try:
                Document.objects.create(
                    stack=stack, number=document['number']
                )
            except BadConnection:
                bad_documents.append(FailedDocument(
                    number=document['number'], stack=stack)
                )

        if Document.objects.filter(stack=stack).exists():
            for document in bad_documents:
                document.save()

            try:
                transaction.savepoint_commit(sid)
            except IntegrityError:
                transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_rollback(sid)