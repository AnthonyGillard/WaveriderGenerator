import math
import unittest
from unittest.mock import patch
from WaveriderGenerator.develop.shock_generator import Wedge


class TestWedge(unittest.TestCase):

    @staticmethod
    def create_dummy_wedge():
        test_wedge = Wedge()
        return test_wedge

    def test_calc_wedge_angle_returns_expected(self):
        wedge = self.create_dummy_wedge()
        shock_angle_rad = math.radians(39.31)
        freestream_mach_number = 2
        expected_wedge_angle_rad = 0.174469904530109

        actual_wedge_angle_rad = wedge._calc_wedge_angle(shock_angle_rad, freestream_mach_number)

        self.assertAlmostEqual(expected_wedge_angle_rad, actual_wedge_angle_rad)

    def test_cot_radians_returns_expected(self):
        test_theta = math.radians(25)
        expected_cot_theta = 2.1445069205095586

        actual_cot_theta = Wedge._cot_radians(test_theta)

        self.assertAlmostEqual(expected_cot_theta, actual_cot_theta)

    def test_mach_squared_x_sine_squared_shock_angle_minus_1_returns_expected(self):
        test_shock_angle_rads = math.pi/4
        test_freestream_mach = 2
        expected_result = 1.0000000000000004

        actual_result = Wedge._mach_squared_x_sine_squared_shock_angle_minus_1(test_shock_angle_rads,
                                                                               test_freestream_mach)

        self.assertAlmostEqual(expected_result, actual_result)

    def test_calculate_shock_angle_returns_expected(self):
        wedge = self.create_dummy_wedge()
        test_wedge_angle = 10
        test_mach_number = 2
        expected_result = 39.31749942144313

        actual_result = wedge.calculate_shock_angle(test_wedge_angle, test_mach_number)

        self.assertAlmostEqual(expected_result, actual_result)
