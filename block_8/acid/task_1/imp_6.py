from typing import List, Dict

from block_8.acid.task_1.exceptions import BadConnection
from block_8.acid.task_1.models import Stack, Document, FailedDocument


def save_stack_of_documents(stack_data: List[Dict]):
    for data in stack_data:
        stack_name, documents = processing_data(data)
        stack_obj = Stack.objects.create(name=stack_name)

        for document in documents:
            document_number = document['number']

            try:
                Document.objects.create(stack=stack_obj, number=document_number)
            except BadConnection:
                FailedDocument.objects.create(stack=stack_obj, number=document_number)

        if Document.objects.filter(stack=stack_obj).count() == 0:
            stack_obj.delete()


def processing_data(data: Dict) -> [str, List]:
    """Обрабатывает входящие данные для получения названия пачки и списка документов."""
    stack: Dict = data['stack']
    stack_name: str = stack['name']
    stack_documents: List = stack['documents']

    return stack_name, stack_documents