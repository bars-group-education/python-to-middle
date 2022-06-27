import inspect
from unittest import TestCase

from block_4.interface_segregation.task_1.implementation import (
    FullTimeDeveloper,
    PartTimeDeveloper,
    ContractDeveloper,
)


class Test(TestCase):

    def _get_salary_method(self, employee):
        for _, method in inspect.getmembers(employee, predicate=inspect.ismethod):
            if hasattr(method, 'salary_method'):
                return method

    def test_full_time(self):
        employee = FullTimeDeveloper()
        self.assertEqual(employee.name, 'FullTimeDeveloper')
        self.assertEqual(self._get_salary_method(employee)(), 110000)

    def test_part_time(self):
        employee = PartTimeDeveloper()
        self.assertEqual(employee.name, 'PartTimeDeveloper')
        self.assertEqual(self._get_salary_method(employee)(), 60000)

    def test_contract(self):
        employee = ContractDeveloper()
        self.assertEqual(employee.name, 'ContractDeveloper')
        self.assertEqual(self._get_salary_method(employee)(), 100000)