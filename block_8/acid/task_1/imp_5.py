from block_8.acid.task_1.exceptions import BadConnection
from block_8.acid.task_1.models import Stack, Document, FailedDocument


def save_stack_of_documents(stack_data):

    for data in stack_data:
        stack = Stack.objects.create(
            name=data["stack"]["name"]
        )
        for document in data["stack"]["documents"]:
            try:
                Document.objects.create(
                    stack=stack,
                    number=document["number"]
                )
            except BadConnection:
                FailedDocument.objects.create(
                    stack=stack,
                    number=document["number"]
                )
        if not Document.objects.exists():
            stack.delete()