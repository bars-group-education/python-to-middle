class Employee:
    """Сотрудник."""

    def __init__(self, salary):
        self.salary = salary
        self.can_develop = False
        self.can_analyze = False
        self.can_test = False


class Developer(Employee):
    """Разработчик"""

    def __init__(self, salary):
        super().__init__(salary)
        self.can_develop = True


class Analyst(Employee):
    """Аналитик"""

    def __init__(self, salary):
        super().__init__(salary)
        self.can_analyze = True


class Tester(Employee):
    """Тестировщик"""

    def __init__(self, salary):
        super().__init__(salary)
        self.can_test = True


class CEO(Developer, Tester, Analyst):
    """Гендиректор"""


class TeamLead(Developer, Tester):
    """Тимлид"""


class ProductOwner(Analyst, Tester):
    """Менеджер продукта"""


class Freelancer:
    """Внештатный сотрудник"""

    def __init__(self, employee):
        self.employee = employee


class Organization:
    """Организация."""

    _can_develop = 0
    _can_analyze = 0
    _can_test = 0
    _total_salary = 0

    @property
    def can_analyze_count(self):
        """Количество сотрудников, которые могут анализировать задачи."""
        return self._can_analyze

    @property
    def can_develop_count(self):
        """Количество сотрудников, которые могут разрабатывать задачи."""
        return self._can_develop

    @property
    def can_test_count(self):
        """Количество сотрудников, которые могут тестировать задачи."""
        return self._can_test

    def accept_employee(self, employee):
        """Принимает сотрудника на работу."""
        if not isinstance(employee, Employee):
            employee = employee.employee
        else:
            self._total_salary += employee.salary

        self._can_analyze += employee.can_analyze
        self._can_test += employee.can_test
        self._can_develop += employee.can_develop

        return self

    def calculate_salary(self):
        """Начисляет заработную плату сотрудникам.

        Returns:
            Возвращает общую сумму всех начислений
        """
        return self._total_salary

    def accept_employees(self, *args):
        """Массовый прием на работу"""

        for arg in args:
            self.accept_employee(arg)