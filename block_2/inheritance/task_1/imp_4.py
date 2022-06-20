class Employee:
    """Сотрудник."""
    def __init__(self, salary):
        self.dev = 0
        self.analyse = 0
        self.test = 0
        self.salary = salary

class CEO(Employee):
    def __init__(self, salary):
        super().__init__(salary)
        self.dev = 1
        self.analyse = 1
        self.test = 1

class Developer(Employee):
    def __init__(self, salary):
        super().__init__(salary)
        self.dev = 1

class Analyst(Employee):
    def __init__(self, salary):
        super().__init__(salary)
        self.analyse = 1

class Tester(Employee):
    def __init__(self, salary):
        super().__init__(salary)
        self.test = 1

class TeamLead(Employee):
    def __init__(self, salary):
        super().__init__(salary)
        self.dev = 1
        self.test = 1

class ProductOwner(Employee):
    def __init__(self, salary):
        super().__init__(salary)
        self.analyse = 1
        self.test = 1

class Freelancer:
    def __init__(self, position):
        self.dev = position.dev
        self.analyse = position.analyse
        self.test = position.test


class Organization:
    """Организация."""

    __analyse = 0
    __dev = 0
    __test = 0
    __total_salary = 0

    @property
    def can_analyze_count(self):
        """Количество сотрудников, которые могут анализировать задачи."""
        return self.__analyse

    @property
    def can_develop_count(self):
        """Количество сотрудников, которые могут разрабатывать задачи."""
        return self.__dev

    @property
    def can_test_count(self):
        """Количество сотрудников, которые могут тестировать задачи."""
        return self.__test

    def accept_employee(self, employee):
        """Принимает сотрудника на работу."""
        if not isinstance(employee, Employee):
            raise TypeError
        if isinstance(employee, CEO):
            self.__analyse += 1
            self.__dev += 1
            self.__test += 1
            self.__total_salary += employee.salary
        elif isinstance(employee, Developer):
            self.__dev += 1
            self.__total_salary += employee.salary
        elif isinstance(employee, Tester):
            self.__test += 1
            self.__total_salary += employee.salary
        elif isinstance(employee, Analyst):
            self.__analyse += 1
            self.__total_salary += employee.salary
        elif isinstance(employee, TeamLead):
            self.__dev += 1
            self.__test += 1
            self.__total_salary += employee.salary
        elif isinstance(employee, ProductOwner):
            self.__analyse += 1
            self.__test += 1
            self.__total_salary += employee.salary
        return self

    def accept_employees(self, *args):
        """Принимает сотрудников на работу."""
        for employee in args:
            if isinstance(employee, CEO):
                self.__analyse += 1
                self.__dev += 1
                self.__test += 1
                self.__total_salary += employee.salary
            elif isinstance(employee, Developer):
                self.__dev += 1
                self.__total_salary += employee.salary
            elif isinstance(employee, Tester):
                self.__test += 1
                self.__total_salary += employee.salary
            elif isinstance(employee, Analyst):
                self.__analyse += 1
                self.__total_salary += employee.salary
            elif isinstance(employee, TeamLead):
                self.__dev += 1
                self.__test += 1
                self.__total_salary += employee.salary
            elif isinstance(employee, ProductOwner):
                self.__analyse += 1
                self.__test += 1
                self.__total_salary += employee.salary
            elif isinstance(employee, ProductOwner):
                self.__analyse += 1
                self.__test += 1
                self.__total_salary += employee.salary
            elif isinstance(employee, Freelancer):
                self.__analyse += employee.analyse
                self.__test += employee.test
                self.__dev += employee.dev

    def calculate_salary(self):
        """Начисляет заработную плату сотрудникам.

        Returns:
            Возвращает общую сумму всех начислений
        """
        return self.__total_salary



