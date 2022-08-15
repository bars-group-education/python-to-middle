from block_8.acid.task_1.models import (
    Stack,
    Document,
    FailedDocument,
)
from block_8.acid.task_1.exceptions import (
    BadConnection,
)


def save_stack_of_documents(stack_data):
    for index, stack in enumerate(stack_data):
        documents = stack_data[index]['stack']['documents']
        tmp_failed_documents = []
        stack = Stack.objects.create(name=stack_data[index]['stack']['name'])
        for document in documents:
            try:
                Document.objects.create(number=document['number'], stack=stack)
            except BadConnection:
                tmp_failed_documents.append(document['number'])
        if Document.objects.exists():
            for tmp_failed_document in tmp_failed_documents:
                FailedDocument.objects.create(number=tmp_failed_document, stack=stack)
        else:
            stack.delete()