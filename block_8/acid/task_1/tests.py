from django.test import (
    TestCase,
)

from block_8.acid.task_1.helpers import (
    set_emulator,
    TrueGenerator,
    SwitchGenerator,
    FalseGenerator,
)
from block_8.acid.task_1.implementation import (
    save_stack_of_documents,
)
from block_8.acid.task_1.models import (
    Stack,
    Document,
    FailedDocument,
)


data = [
    {
        "stack": {
            "name": "Пачка",
            "documents": [
                {
                    "number": "1"
                },
                {
                    "number": "2"
                },
                {
                    "number": "3"
                },
                {
                    "number": "4"
                },
                {
                    "number": "5"
                },
                {
                    "number": "6"
                },
                {
                    "number": "7"
                },
                {
                    "number": "8"
                },
                {
                    "number": "9"
                },
                {
                    "number": "10"
                }
            ]
        }
    }
]


class MyTestCase(TestCase):

    def test_all_docs(self):
        set_emulator(TrueGenerator())
        save_stack_of_documents(data)
        self.assertEqual(Stack.objects.count(), 1)
        self.assertEqual(Document.objects.count(), 10)
        self.assertEqual(FailedDocument.objects.count(), 0)

    def test_half_docs(self):
        set_emulator(SwitchGenerator())
        save_stack_of_documents(data)
        self.assertEqual(Stack.objects.count(), 1)
        self.assertEqual(Document.objects.count(), 5)
        self.assertEqual(FailedDocument.objects.count(), 5)

    def test_no_one_docs(self):
        set_emulator(FalseGenerator())
        save_stack_of_documents(data)
        self.assertEqual(Stack.objects.count(), 0)
        self.assertEqual(Document.objects.count(), 0)
        self.assertEqual(FailedDocument.objects.count(), 0)
