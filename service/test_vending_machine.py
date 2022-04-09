from unittest import TestCase

from service.vending_machine import validate_deposit


class TestVendingMachineService(TestCase):
    def test_validate_deposit(self):
        false_test_cases = [0, 1, 2, 3, 4, 4.5, 7, 23, 15, 30, 35, 40]
        true_test_cases = [5, 10, 20, 50, 100]

        for it in false_test_cases:
            res, message = validate_deposit(it)
            self.assertFalse(res)

        for it in true_test_cases:
            res, message = validate_deposit(it)
            self.assertTrue(res)
