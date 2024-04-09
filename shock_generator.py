import math
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import matplotlib.tri as tri


class Wedge:
    SPECIFIC_HEAT_RATIO = 1.4
    OUT_OF_PLANE_INCREMENT = 0.1

    def __init__(self, wedge_angle, freesteam_mach_number, width=10, length=2):
        self.wedge_angle = math.radians(wedge_angle)
        self.freesteam_mach_number = freesteam_mach_number
        self.width = 10
        self.length = 2

        # self._calculate_shock_angle()

        self.plot()

    def _calculate_shock_angle(self):
        shock_angles = np.linspace(1, 45, 441)
        #print(shock_angles)

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

    def plot(self):
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        x = np.array([0, self.length+self.OUT_OF_PLANE_INCREMENT, 0, self.length+self.OUT_OF_PLANE_INCREMENT])
        y = np.array([-self.width/2-self.OUT_OF_PLANE_INCREMENT, -self.width/2-self.OUT_OF_PLANE_INCREMENT,
                      self.width/2+self.OUT_OF_PLANE_INCREMENT, self.width/2+self.OUT_OF_PLANE_INCREMENT])
        z = x * 0
        base = self.plot_triangular_surface(ax, x, y, z)

        x = np.array([0, self.length, 0, self.length])
        y = np.array([-self.width / 2 - self.OUT_OF_PLANE_INCREMENT, -self.width / 2,
                      self.width / 2 + self.OUT_OF_PLANE_INCREMENT, self.width / 2])
        z = x * -math.tan(self.wedge_angle)
        hypotenuse = self.plot_triangular_surface(ax, x, y, z)

        x = np.array([0, self.length+self.OUT_OF_PLANE_INCREMENT, self.length])
        y = np.array([-self.width/2-self.OUT_OF_PLANE_INCREMENT, -self.width/2-self.OUT_OF_PLANE_INCREMENT,
                      -self.width/2])
        z = np.array(([0, 0, self.length * -math.tan(self.wedge_angle)]))
        neg_side = self.plot_triangular_surface(ax, x, y, z)

        y = y * -1
        pos_side = self.plot_triangular_surface(ax, x, y, z)

        x = np.array([self.length, self.length + self.OUT_OF_PLANE_INCREMENT, self.length,
                      self.length + self.OUT_OF_PLANE_INCREMENT])
        y = np.array([-self.width/2, -self.width/2 - self.OUT_OF_PLANE_INCREMENT, self.width / 2,
                      self.width/2 + self.OUT_OF_PLANE_INCREMENT])
        z = np.array([self.length * -math.tan(self.wedge_angle), 0, self.length * -math.tan(self.wedge_angle), 0])
        back = self.plot_triangular_surface(ax, x, y, z)

        ax.set_xlim(0, 2.5)
        ax.set_ylim(-self.width/2-self.OUT_OF_PLANE_INCREMENT, self.width/2+self.OUT_OF_PLANE_INCREMENT)
        ax.set_zlim(-0.5, 0.5)

        plt.show()

    @staticmethod
    def plot_triangular_surface(axis, x, y, z, _color='b', _antialiased=True, _alpha=1.0):
        return axis.plot_trisurf(x, y, z, color=_color, antialiased=_antialiased, alpha=_alpha, edgecolor='black')


if __name__ == "__main__":
    wedge = Wedge(5, 5.0)
