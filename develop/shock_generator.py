import math
import numpy as np
from scipy.optimize import minimize


class ShockGenerator:
    SAMPLING_NO = 6
    MIN_ANGLE = 40
    MAX_ANGLE = 45
    SPECIFIC_HEAT_RATIO = 1.4


class Wedge(ShockGenerator):
    OUT_OF_PLANE_INCREMENT = 0.1

    def __init__(self, wedge_angle, freesteam_mach_number):
        self.wedge_angle = math.radians(wedge_angle)
        self.freesteam_mach_number = freesteam_mach_number
        self.width = 10
        self.length = 2

        self._calculate_shock_angle()

    def _calculate_shock_angle(self):
        shock_angles = np.linspace(self.MIN_ANGLE, self.MAX_ANGLE, self.SAMPLING_NO)
        wedge_angles = np.zeros(shock_angles.shape)

        print(shock_angles)

        for index, shock_angle in enumerate(shock_angles):
            shock_angles[index] = math.radians(shock_angle)
            wedge_angles[index] = math.degrees(self._calc_wedge_angle(shock_angles[index]))

        print(wedge_angles)

    def _calc_wedge_angle(self, shock_angle):
        cot_shock = self._cot(shock_angle)
        eqn_numerator = self._mach_squared_x_sine_squared_shock_angle_minus_1(shock_angle)
        eqn_denominator = (((self.SPECIFIC_HEAT_RATIO + 1) / 2) * (self.freesteam_mach_number ** 2)) - eqn_numerator

        return math.atan(cot_shock * (eqn_numerator / eqn_denominator))

    def _wedge_shock_angle_relationship(self, shock_angle, wedge_angle):
        shock_angle = shock_angle[0]
        return (self._cot(shock_angle) *
                (self._mach_squared_x_sine_squared_shock_angle_minus_1(shock_angle) /
                 (((self.SPECIFIC_HEAT_RATIO - 1) / 2) * (self.freesteam_mach_number ** 2) -
                  self._mach_squared_x_sine_squared_shock_angle_minus_1(shock_angle)))) - math.tan(wedge_angle)

    @staticmethod
    def _cot(theta_radians):
        return math.cos(theta_radians) / math.sin(theta_radians)

    def _mach_squared_x_sine_squared_shock_angle_minus_1(self, shock_angle):
        return ((self.freesteam_mach_number ** 2) * (math.sin(shock_angle) ** 2)) - 1


class Cone(ShockGenerator):
    pass


class Imported(ShockGenerator):
    pass
