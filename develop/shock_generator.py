import math
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
from scipy.optimize import minimize
from WaveriderGenerator.develop.utility import InputValidation


class ShockGenerator:
    SAMPLING_NO = 64
    MIN_SHOCK_ANGLE_DEGREES = 1
    MAX_SHOCK_ANGLE_DEGREES = 64  # Maximum weak shock angle for Mach 2 wedge deflection
    SPECIFIC_HEAT_RATIO = 1.4
    PLOT_FONT = {'fontname': 'Times New Roman'}

    def _plot_deflection_shock_angle_relationship(self, x, y, x_max, y_max, title):
        figure, axis = plt.subplots()
        axis.plot(x, y, color='k')
        axis.set_xlim([0, x_max])
        axis.set_ylim([0, y_max])
        axis.set_title(title, **self.PLOT_FONT)
        axis.set_xlabel('Deflection Angle [$^\circ$]', **self.PLOT_FONT)
        axis.set_ylabel('Weak Shock Angle [$^\circ$]', **self.PLOT_FONT)

        for tick in axis.get_xticklabels():
            tick.set_fontname(self.PLOT_FONT['fontname'])
        for tick in axis.get_yticklabels():
            tick.set_fontname(self.PLOT_FONT['fontname'])

        axis.grid(True, linestyle='--', alpha=0.75, which='both')
        axis.minorticks_on()
        plt.show()

    def _plot_deflection_shock_angle_mach_number_relation_ship(self, x, y, z, x_max, y_max, z_max):
        figure, axis = plt.subplots(subplot_kw={"projection": "3d"})
        surf = axis.plot_surface(x, y, z, linewidth=0, antialiased=False)
        axis.set_xlim([0, x_max])
        axis.set_ylim([0, y_max])
        axis.set_zlim([0, z_max])
        axis.set_xlabel('Deflection Angle [$^\circ$]', **self.PLOT_FONT)
        axis.set_ylabel('Mach Number', **self.PLOT_FONT)
        axis.set_zlabel('Weak Shock Angle [$^\circ$]', **self.PLOT_FONT)
        axis.set_title(f'Oblique Shock Qualities: $\gamma$ = {self.SPECIFIC_HEAT_RATIO}', **self.PLOT_FONT)

        for tick in axis.get_xticklabels():
            tick.set_fontname(self.PLOT_FONT['fontname'])
        for tick in axis.get_yticklabels():
            tick.set_fontname(self.PLOT_FONT['fontname'])
        for tick in axis.get_zticklabels():
            tick.set_fontname(self.PLOT_FONT['fontname'])

        axis.grid(True, linestyle='--', alpha=0.75, which='both')
        axis.minorticks_on()
        plt.show()


class Wedge(ShockGenerator):
    MIN_WEDGE_ANGLE_DEGREES = 0
    MAX_WEDGE_ANGLE_DEGREES = 45
    WEDGE_ANGLE_SAMPLE_RATE = 46
    MIN_MACH_NUMBER = 2
    MAX_MACH_NUMBER = 25
    MACH_NUMBER_SAMPLE_RATE = 24

    def __init__(self):
        pass

    def calculate_shock_angle(self, wedge_angle_degrees, freestream_mach_number):
        InputValidation.assert_input_within_allowable_range(wedge_angle_degrees, self.MIN_WEDGE_ANGLE_DEGREES,
                                                            self.MAX_WEDGE_ANGLE_DEGREES, 'Wedge Angle')
        InputValidation.assert_input_within_allowable_range(freestream_mach_number, self.MIN_MACH_NUMBER,
                                                            self.MAX_MACH_NUMBER, 'Mach Number')

        shock_angles_degrees = np.linspace(self.MIN_SHOCK_ANGLE_DEGREES, self.MAX_SHOCK_ANGLE_DEGREES, self.SAMPLING_NO)
        wedge_angles_degrees = np.zeros(shock_angles_degrees.shape)

        for index, shock_angle_degrees in enumerate(shock_angles_degrees):
            wedge_angles_degrees[index] = math.degrees(self._calc_wedge_angle(math.radians(shock_angle_degrees),
                                                                              freestream_mach_number))

        shock_angle_degrees = np.interp(wedge_angle_degrees, wedge_angles_degrees, shock_angles_degrees, right=np.NAN)

        return shock_angle_degrees

    def plot_deflection_shock_angle_relationship(self, freestream_mach_number):
        wedge_angles_degrees = np.linspace(self.MIN_WEDGE_ANGLE_DEGREES, self.MAX_WEDGE_ANGLE_DEGREES,
                                           self.WEDGE_ANGLE_SAMPLE_RATE)
        shock_angles_degrees = np.zeros(wedge_angles_degrees.shape)

        for index, wedge_angle_degrees in enumerate(wedge_angles_degrees):
            shock_angles_degrees[index] = self.calculate_shock_angle(wedge_angle_degrees, freestream_mach_number)

        title = f'Oblique Shock Qualities: Mach = {freestream_mach_number}, $\gamma$ = {self.SPECIFIC_HEAT_RATIO}'
        self._plot_deflection_shock_angle_relationship(wedge_angles_degrees, shock_angles_degrees,
                                                       self.MAX_WEDGE_ANGLE_DEGREES, self.MAX_SHOCK_ANGLE_DEGREES,
                                                       title)

    def plot_deflection_shock_angle_mach_number_relationship(self):
        wedge_angles_degrees = np.linspace(self.MIN_WEDGE_ANGLE_DEGREES, self.MAX_WEDGE_ANGLE_DEGREES,
                                           self.WEDGE_ANGLE_SAMPLE_RATE)
        mach_numbers = np.linspace(self.MIN_MACH_NUMBER, self.MAX_MACH_NUMBER, self.MACH_NUMBER_SAMPLE_RATE)

        wedge_angles_degrees, mach_numbers = np.meshgrid(wedge_angles_degrees, mach_numbers)
        vectorised_calc_shock_angle = np.vectorize(self.calculate_shock_angle)
        shock_angles = vectorised_calc_shock_angle(wedge_angles_degrees, mach_numbers)

        self._plot_deflection_shock_angle_mach_number_relation_ship(wedge_angles_degrees, mach_numbers, shock_angles,
                                                                    self.MAX_WEDGE_ANGLE_DEGREES, self.MAX_MACH_NUMBER,
                                                                    self.MAX_SHOCK_ANGLE_DEGREES)

    def _calc_wedge_angle(self, shock_angle_radians, freestream_mach_number):
        cot_shock = self._cot_radians(shock_angle_radians)
        eqn_numerator = self._mach_squared_x_sine_squared_shock_angle_minus_1(shock_angle_radians,
                                                                              freestream_mach_number)
        eqn_denominator = (((self.SPECIFIC_HEAT_RATIO + 1) / 2) * (freestream_mach_number ** 2)) - eqn_numerator
        return math.atan(cot_shock * (eqn_numerator / eqn_denominator))

    @staticmethod
    def _cot_radians(theta_radians):
        return math.cos(theta_radians) / math.sin(theta_radians)

    @staticmethod
    def _mach_squared_x_sine_squared_shock_angle_minus_1(shock_angle_radians, freestream_mach_number):
        return ((freestream_mach_number ** 2) * (math.sin(shock_angle_radians) ** 2)) - 1


class Cone(ShockGenerator):
    pass


class Imported(ShockGenerator):
    pass
