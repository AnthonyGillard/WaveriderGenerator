import math
import unittest
from unittest.mock import patch
from WaveriderGenerator.develop.utility import InputValidation


class TestInputValidation(unittest.TestCase):

    def test_assert_input_within_allowable_range_raise_exception_when_input_less_than_min(self):
        test_input = 10
        test_name = 'test'
        test_min = 20
        test_max = 40

        with self.assertRaises(ValueError) as exception_context:
            InputValidation.assert_input_within_allowable_range(test_input, test_min, test_max, test_name)
        self.assertEqual(f'{test_name}, ({test_input}) is not within allowable bounds. '
                         f'Minimum value accepted = {test_min}, maximum value accepted = {test_max}',
                         str(exception_context.exception))

    def test_assert_input_within_allowable_range_raise_exception_when_input_more_than_max(self):
        test_input = 50
        test_name = 'test'
        test_min = 20
        test_max = 40

        with self.assertRaises(ValueError) as exception_context:
            InputValidation.assert_input_within_allowable_range(test_input, test_min, test_max, test_name)
        self.assertEqual(f'{test_name}, ({test_input}) is not within allowable bounds. '
                         f'Minimum value accepted = {test_min}, maximum value accepted = {test_max}',
                         str(exception_context.exception))

