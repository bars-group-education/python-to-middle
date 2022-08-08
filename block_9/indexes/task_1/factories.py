from faker import Faker
from django.core import serializers

from block_9.indexes.task_1.models import Employee

faker = Faker(locale='ru-RU')


def generate_data():

    employee = Employee()
    employee.inn = faker.ssn()
    employee.fname, employee.iname, employee.oname = faker.name().split(' ')
    employee.department_id = faker.random_int(0, 100)
    employee.position_id = faker.random_int(0, 100)
    employee.begin = faker.date_this_century()
    employee.end = faker.date_between(start_date='+10y', end_date='+40y')
    employee.additional_info = faker.text()
    pass

generate_data()