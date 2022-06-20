from enum import Enum
from enum import auto
from operator import attrgetter


class Skill(Enum):
    TEST = auto()
    DEVELOP = auto()
    ANALYZE = auto()


class Employee:
    """Сотрудник."""

    def __init__(self, salary) -> None:
        self.salary = salary

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}: {self.salary}>'


class CEO(Employee):
    """Генеральный директор."""

    skills = (Skill.ANALYZE, Skill.DEVELOP, Skill.TEST)


class Developer(Employee):
    """Разработчик."""

    skills = (Skill.DEVELOP,)


class Analyst(Employee):
    """Аналитик."""

    skills = (Skill.ANALYZE,)


class Tester(Employee):
    """Тестировщик."""

    skills = (Skill.TEST,)


class TeamLead(Employee):
    """ТимЛид."""

    skills = (Skill.DEVELOP, Skill.TEST)


class ProductOwner(Employee):
    """Менеджер продукта."""

    skills = (Skill.ANALYZE, Skill.TEST)


class Freelancer(Employee):
    """Внештатный сотрудник."""

    def __init__(self, job) -> None:
        self.__job = job

    def __getattr__(self, name):
        if name == 'salary':
            return 0
        return getattr(self.__job, name)


class Organization:
    """Организация."""

    def __init__(self) -> None:
        self._employees = []

    def _calculate_skill_count(self, skill: Skill) -> int:
        return sum(
            1 for employee in self._employees if skill in employee.skills
        )

    @property
    def can_analyze_count(self):
        """Количество сотрудников, которые могут анализировать задачи."""
        return self._calculate_skill_count(Skill.ANALYZE)

    @property
    def can_develop_count(self):
        """Количество сотрудников, которые могут разрабатывать задачи."""
        return self._calculate_skill_count(Skill.DEVELOP)

    @property
    def can_test_count(self):
        """Количество сотрудников, которые могут тестировать задачи."""
        return self._calculate_skill_count(Skill.TEST)

    def accept_employee(self, employee):
        """Принимает сотрудника на работу."""
        if not isinstance(employee, Employee):
            raise TypeError
        self._employees.append(employee)
        return self

    def accept_employees(self, *employees) -> None:
        for employee in employees:
            self.accept_employee(employee)

    def calculate_salary(self) -> int:
        """Начисляет заработную плату сотрудникам.

        Returns:
            Возвращает общую сумму всех начислений
        """
        return sum(map(attrgetter('salary'), self._employees))