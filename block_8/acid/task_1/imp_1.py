from django.db import transaction

from .exceptions import BadConnection, BadData
from .models import Stack, Document, FailedDocument


@transaction.atomic
def save_stack_of_documents(stack_data):

    try:
        stack = stack_data[0].get('stack')
        docs = stack.get('documents')
        name = stack.get('name')
        if None in (docs, name):
            raise BadData
    except IndexError:
        raise BadData

    new_stack = Stack.objects.create(name=name)

    for doc in docs:
        try:
            Document.objects.create(stack=new_stack, number=doc.get('number'))
        except BadConnection:
            FailedDocument.objects.create(stack=new_stack, number=doc.get('number'))

    valid_docs = Document.objects.filter(stack=new_stack, valid=True).exists()
    if not valid_docs:
        transaction.set_rollback(True)