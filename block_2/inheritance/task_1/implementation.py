class Employee:
    """Сотрудник."""


class Organization:
    """Организация."""

    @property
    def can_analyze_count(self):
        """Количество сотрудников, которые могут анализировать задачи."""
        raise NotImplementedError

    @property
    def can_develop_count(self):
        """Количество сотрудников, которые могут разрабатывать задачи."""
        raise NotImplementedError

    @property
    def can_test_count(self):
        """Количество сотрудников, которые могут тестировать задачи."""
        raise NotImplementedError

    def accept_employee(self, employee):
        """Принимает сотрудника на работу."""
        if not isinstance(employee, Employee):
            raise TypeError

    def calculate_salary(self):
        """Начисляет заработную плату сотрудникам.

        Returns:
            Возвращает общую сумму всех начислений
        """
        raise NotImplementedError




