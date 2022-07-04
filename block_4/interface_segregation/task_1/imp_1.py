def salary_method(f):
    f.salary_method = True

    return f


class Name:

    @property
    def name(self):
        raise NotImplementedError


class MonthlySalary:

    def monthly_salary(self):
        raise NotImplementedError


class OtherBenefits:

    @property
    def other_benefits(self):
        raise NotImplementedError


class HourlyRate:

    @property
    def hourly_rate(self):
        raise NotImplementedError


class HoursInMonth:

    @property
    def hours_in_month(self):
        raise NotImplementedError


class CalculateMonthSalary:

    @salary_method
    def calculate_month_salary(self):
        raise NotImplementedError


class CalculateContractSalary:

    @salary_method
    def calculate_contract_salary(self):
        raise NotImplementedError


class FullTimeDeveloper(Name, MonthlySalary, OtherBenefits, CalculateMonthSalary):

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


class PartTimeDeveloper(Name, MonthlySalary, OtherBenefits, HoursInMonth, CalculateMonthSalary):

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


class ContractDeveloper(Name, HourlyRate, HoursInMonth, CalculateMonthSalary):

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
    def calculate_month_salary(self):

        return self.hourly_rate * self.hours_in_month