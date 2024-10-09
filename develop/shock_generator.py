import math
import numpy as np
from scipy.optimize import minimize


class ShockGenerator:
    pass


class Wedge(ShockGenerator):
    SPECIFIC_HEAT_RATIO = 1.4
    OUT_OF_PLANE_INCREMENT = 0.1

    def __init__(self, wedge_angle, freesteam_mach_number):
        self.wedge_angle = math.radians(wedge_angle)
        self.freesteam_mach_number = freesteam_mach_number
        self.width = 10
        self.length = 2

        # self._calculate_shock_angle()

    def _calculate_shock_angle(self):
        shock_angles = np.linspace(1, 45, 441)

        print(minimize(self._wedge_shock_angle_relationship, np.array([5]), args=(self.wedge_angle)))

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
        return (self.freesteam_mach_number ** 2 * math.sin(shock_angle) ** 2) - 1


class Cone(ShockGenerator):
    pass


class Imported(ShockGenerator):
    pass
