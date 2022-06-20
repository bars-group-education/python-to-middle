from typing import Iterable


class Employee:
    """Сотрудник."""

    def __init__(self, salary) -> None:
        super().__init__()
        self.salary = salary


class CEO(Employee):
    """Генеральный директор."""

    def __init__(self, salary) -> None:
        super().__init__(salary)

        self.analyze = True
        self.develop = True
        self.test = True


class Developer(Employee):
    """Разработчик."""

    def __init__(self, salary) -> None:
        super().__init__(salary)

        self.develop = True


class Analyst(Employee):
    """Аналитик."""

    def __init__(self, salary) -> None:
        super().__init__(salary)

        self.analyze = True


class Tester(Employee):
    """Тестировщик."""

    def __init__(self, salary) -> None:
        super().__init__(salary)

        self.test = True


class TeamLead(Employee):
    """ТимЛид."""

    def __init__(self, salary) -> None:
        super().__init__(salary)

        self.develop = True
        self.test = True


class ProductOwner(Employee):
    """Менеджер продукта."""

    def __init__(self, salary) -> None:
        super().__init__(salary)

        self.analyze = True
        self.test = True


class Freelancer(Employee):
    """Внештатный сотрудник."""

    def __init__(self, parent):
        self.parent = parent
        self.salary = 0

    def __getattr__(self, name):
        if name is 'salary':
            return self.salalry
        else:
            return getattr(self.parent, name)


class Organization:
    """Организация."""

    def __init__(self) -> None:
        super().__init__()
        self.employers = []
        self.can = {
            'analyze': 0,
            'develop': 0,
            'test': 0,
        }

    @property
    def can_analyze_count(self):
        """Количество сотрудников, которые могут анализировать задачи."""
        return self.can['analyze']

    @property
    def can_develop_count(self):
        """Количество сотрудников, которые могут разрабатывать задачи."""
        return self.can['develop']

    @property
    def can_test_count(self):
        """Количество сотрудников, которые могут тестировать задачи."""
        return self.can['test']

    def accept_employee(self, employee):
        """Принимает сотрудника на работу."""
        if not isinstance(employee, Employee):
            raise TypeError
        self.employers.append(employee)
        for can in self.can.keys():
            if hasattr(employee, can):
                self.can[can] += 1
        return self

    def accept_employees(self, *employees):
        """Принимает сотрудника на работу."""
        if not isinstance(employees, Iterable):
            raise TypeError
        for employee in employees:
            self.accept_employee(employee)

    def calculate_salary(self):
        """Начисляет заработную плату сотрудникам.

        Returns:
            Возвращает общую сумму всех начислений
        """
        common_salary = 0

        for employee in self.employers:
            common_salary += employee.salary

        return common_salary
