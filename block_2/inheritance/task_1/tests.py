from unittest import TestCase

from block_2.inheritance.task_1.implementation import (
    Organization,
    CEO,  # Генеральный директор
    Developer,  # Разработчик
    Analyst,  # Аналитик
    Tester,  # Тестеровщик
    TeamLead,  # ТимЛид
    ProductOwner,  # Менеджер продукта
    Freelancer,  # Внештатный сотрудник
)


class Test(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.org = Organization()
        self.ceo = CEO(1000000)
        self.developer = Developer(300000)
        self.analyst = Analyst(100000)
        self.tester = Tester(200000)
        self.team_lead = TeamLead(500000)
        self.product_owner = ProductOwner(400000)

    def test_ceo_only(self):
        self.org.accept_employee(self.ceo)

        self.assertEqual(self.org.can_develop_count, 1)
        self.assertEqual(self.org.can_analyze_count, 1)
        self.assertEqual(self.org.can_test_count, 1)
        self.assertEqual(self.org.calculate_salary(), 1000000)

    def test_one_per_skill(self):
        self.org.accept_employees(self.ceo, self.developer, self.analyst, self.tester)

        self.assertEqual(self.org.can_develop_count, 2)
        self.assertEqual(self.org.can_analyze_count, 2)
        self.assertEqual(self.org.can_test_count, 2)
        self.assertEqual(self.org.calculate_salary(), 1600000)

    def test_with_team_lead_and_product_owner(self):
        self.org.accept_employee(
            self.ceo,
        ).accept_employee(
            self.developer,
        ).accept_employee(
            self.analyst,
        ).accept_employee(
            self.tester,
        ).accept_employee(
            self.team_lead,
        ).accept_employee(
            self.product_owner,
        )

        self.assertEqual(self.org.can_develop_count, 3)
        self.assertEqual(self.org.can_analyze_count, 3)
        self.assertEqual(self.org.can_test_count, 4)
        self.assertEqual(self.org.calculate_salary(), 2500000)

    def test_with_freelancers(self):
        self.org.accept_employees(
            self.ceo,
            self.developer,
            self.analyst,
            self.tester,
            self.team_lead,
            self.product_owner,
            Freelancer(self.developer),
            Freelancer(self.analyst),
            Freelancer(self.tester),
        )

        self.assertEqual(self.org.can_develop_count, 4)
        self.assertEqual(self.org.can_analyze_count, 4)
        self.assertEqual(self.org.can_test_count, 5)
        self.assertEqual(self.org.calculate_salary(), 2500000)
