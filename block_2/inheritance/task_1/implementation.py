class Employee:
    """Сотрудник."""

    def get_salary(self):
        raise NotImplementedError


class Freelancer(Employee):

    def __init__(self, employee) -> None:
        super().__init__()
        self._employee = employee

    @property
    def __class__(self):
        return self._employee.__class__

    def get_salary(self):
        return 0


class StaffEmployee(Employee):
    """Штатный сотрудник"""

    def __init__(self, salary) -> None:
        super().__init__()
        self._salary = salary

    def get_salary(self):
        return self._salary


class DeveloperRole:
    pass


class AnalystRole:
    pass


class TesterRole:
    pass


class CEO(StaffEmployee, DeveloperRole, AnalystRole, TesterRole):
    """Генеральный директор"""


class Developer(StaffEmployee, DeveloperRole):
    """Разработчик"""


class Analyst(StaffEmployee, AnalystRole):
    """Аналитик"""


class Tester(StaffEmployee, TesterRole):
    """Тестеровщик"""


class TeamLead(StaffEmployee, DeveloperRole, TesterRole):
    """ТимЛид"""


class ProductOwner(StaffEmployee, AnalystRole, TesterRole):
    """Владелец продукта"""


class Organization:
    """Организация."""

    def __init__(self) -> None:
        super().__init__()
        self._employees = []

    @property
    def can_analyze_count(self):
        """Количество сотрудников, которые могут анализировать задачи."""
        return self._calc_with_role(AnalystRole)

    @property
    def can_develop_count(self):
        """Количество сотрудников, которые могут разрабатывать задачи."""
        return self._calc_with_role(DeveloperRole)

    @property
    def can_test_count(self):
        """Количество сотрудников, которые могут тестировать задачи."""
        return self._calc_with_role(TesterRole)

    def _calc_with_role(self, role):
        counter = 0

        for employee in self._employees:
            if isinstance(employee, role):
                counter += 1

        return counter

    def accept_employee(self, employee):
        """Принимает сотрудника на работу."""
        if not isinstance(employee, Employee):
            raise TypeError

        self._employees.append(employee)

        return self

    def accept_employees(self, *employees):
        for employee in employees:
            self.accept_employee(employee)

    def calculate_salary(self):
        """Начисляет заработную плату сотрудникам.

        Returns:
            Возвращает общую сумму всех начислений
        """
        return sum(x.get_salary() for x in self._employees)
