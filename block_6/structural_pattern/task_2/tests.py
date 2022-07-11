import unittest

from block_6.structural_pattern.task_2.implementation import Driver


class MyTestCase(unittest.TestCase):

    def test_car_start_use(self):
        driver = Driver()
        driver.start_use()

        self.assertEqual(driver.car.state['open_car'], True)
        self.assertEqual(driver.car.state['moving'], True)
        self.assertEqual(driver.car.state['engine_work'], True)

    def test_car_stop_use(self):
        driver = Driver()
        driver.start_use()
        driver.stop_use()

        self.assertEqual(driver.car.state['open_car'], False)
        self.assertEqual(driver.car.state['moving'], False)
        self.assertEqual(driver.car.state['engine_work'], False)
