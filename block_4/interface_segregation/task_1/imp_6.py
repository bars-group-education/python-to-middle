def salary_method(f):
    f.salary_method = True

    return f


class Employee:
    @property
    def name(self):
        raise NotImplementedError


class Staff:
    @property
    def monthly_salary(self):
        raise NotImplementedError

    @property
    def other_benefits(self):
        raise NotImplementedError

    @salary_method
    def calculate_month_salary(self):
        raise NotImplementedError


class HoursDependingEmployee:
    @property
    def hours_in_month(self):
        raise NotImplementedError


class Contract:
    @property
    def hourly_rate(self):
        raise NotImplementedError

    @salary_method
    def calculate_contract_salary(self):
        raise NotImplementedError


class FullTimeDeveloper(Employee, Staff):

    @property
    def name(self):
        return self.__class__.__name__

    @property
    def monthly_salary(self):
        return 100000

    @property
    def other_benefits(self):
        return 10000

    @salary_method
    def calculate_month_salary(self):
        return self.monthly_salary + self.other_benefits


class PartTimeDeveloper(Employee, Staff, HoursDependingEmployee):

    @property
    def name(self):
        return self.__class__.__name__

    @property
    def monthly_salary(self):
        return 100000

    @property
    def other_benefits(self):
        return 10000

    @property
    def hours_in_month(self):
        return 100.0

    @salary_method
    def calculate_month_salary(self):
        return self.monthly_salary / 200.0 * self.hours_in_month + self.other_benefits


class ContractDeveloper(Employee, Contract, HoursDependingEmployee):

    @property
    def name(self):
        return self.__class__.__name__

    @property
    def hourly_rate(self):
        return 1000

    @property
    def hours_in_month(self):
        return 100.0

    @salary_method
    def calculate_contract_salary(self):
        return self.hourly_rate * self.hours_in_month