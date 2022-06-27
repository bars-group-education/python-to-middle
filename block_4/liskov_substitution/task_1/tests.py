from inspect import getmembers, isclass
from unittest import TestCase

from block_4.liskov_substitution.task_1 import implementation as imp


class Test(TestCase):

    def test(self):
        for _, member in getmembers(imp, predicate=isclass):
            if issubclass(member, imp.BaseAccountClass) and not (member is imp.BaseAccountClass):
                account = member()
                account.deposit(1000)
                account.withdraw(1000)

