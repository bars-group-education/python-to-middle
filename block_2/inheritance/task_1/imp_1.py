class Employee:
    """Сотрудник."""

    def __init__(self, salary):
        self.salary = salary
        self.skill = None


class Organization:

    """Организация."""
    def __init__(self):
        self.employees = set()

    @property
    def can_analyze_count(self):
        """Количество сотрудников, которые могут анализировать задачи."""
        return len([True for employee in self.employees if hasattr(employee, 'analyze')])

    @property
    def can_develop_count(self):
        """Количество сотрудников, которые могут разрабатывать задачи."""
        return len([True for employee in self.employees if hasattr(employee, 'develop')])

    @property
    def can_test_count(self):
        """Количество сотрудников, которые могут тестировать задачи."""
        return len([True for employee in self.employees if hasattr(employee, 'test')])

    def accept_employee(self, employee):
        """Принимает сотрудника на работу."""
        if not isinstance(employee, Employee):
            raise TypeError

        self.employees.add(employee)

        return self

    def accept_employees(self, *employees):
        """Принимает сотрудников на работу."""
        departments = {}

        for employee in employees:
            self.accept_employee(employee)

    def calculate_salary(self):
        """Начисляет заработную плату сотрудникам.

        Returns:
            Возвращает общую сумму всех начислений
        """
        return sum([employee.salary for employee in self.employees if hasattr(employee, 'salary')])


class Analyst(Employee):

    def analyze(self):
        pass


class Developer(Employee):

    def develop(self):
        pass


class Tester(Employee):

    def test(self):
        pass


class CEO(Analyst, Developer, Tester):
    pass


class TeamLead(Developer, Tester):
    pass


class ProductOwner(Analyst, Tester):
    pass


class Freelancer:
    def __new__(cls, *args, **kwargs):
        return super().__new__(args[0].__class__)
