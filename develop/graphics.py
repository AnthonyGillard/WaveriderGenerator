import matplotlib.pyplot as plt
import matplotlib.tri as tri
import numpy as np
import math


class GraphicsGenerator:
    WIDTH = 10
    LENGTH = 2
    OUT_OF_PLANE_INCREMENT = 0.1

    def __init__(self):
        self.figure, self.axis = plt.subplots(subplot_kw={"projection": "3d"})

    def plot_wedge(self, wedge_angle):
        x = np.array([0, self.LENGTH + self.OUT_OF_PLANE_INCREMENT, 0, self.LENGTH + self.OUT_OF_PLANE_INCREMENT])
        y = np.array([-self.WIDTH / 2 - self.OUT_OF_PLANE_INCREMENT, -self.WIDTH / 2 - self.OUT_OF_PLANE_INCREMENT,
                      self.WIDTH / 2 + self.OUT_OF_PLANE_INCREMENT, self.WIDTH / 2 + self.OUT_OF_PLANE_INCREMENT])
        z = x * 0
        base = self._create_triangular_surface(x, y, z)

        x = np.array([0, self.LENGTH, 0, self.LENGTH])
        y = np.array([-self.WIDTH / 2 - self.OUT_OF_PLANE_INCREMENT, -self.WIDTH / 2,
                      self.WIDTH / 2 + self.OUT_OF_PLANE_INCREMENT, self.WIDTH / 2])
        z = x * -math.tan(wedge_angle)
        hypotenuse = self._create_triangular_surface(x, y, z)

        x = np.array([0, self.LENGTH + self.OUT_OF_PLANE_INCREMENT, self.LENGTH])
        y = np.array([-self.WIDTH / 2 - self.OUT_OF_PLANE_INCREMENT, -self.WIDTH / 2 - self.OUT_OF_PLANE_INCREMENT,
                      -self.WIDTH / 2])
        z = np.array(([0, 0, self.LENGTH * -math.tan(wedge_angle)]))
        neg_side = self._create_triangular_surface(x, y, z)

        y = y * -1
        pos_side = self._create_triangular_surface(x, y, z)

        x = np.array([self.LENGTH, self.LENGTH + self.OUT_OF_PLANE_INCREMENT, self.LENGTH,
                      self.LENGTH + self.OUT_OF_PLANE_INCREMENT])
        y = np.array([-self.WIDTH / 2, -self.WIDTH / 2 - self.OUT_OF_PLANE_INCREMENT, self.WIDTH / 2,
                      self.WIDTH / 2 + self.OUT_OF_PLANE_INCREMENT])
        z = np.array([self.LENGTH * -math.tan(wedge_angle), 0, self.LENGTH * -math.tan(wedge_angle), 0])
        back = self._create_triangular_surface(x, y, z)

        self.axis.set_xlim(0, 2.5)
        self.axis.set_ylim(-self.WIDTH / 2 - self.OUT_OF_PLANE_INCREMENT, self.WIDTH / 2 + self.OUT_OF_PLANE_INCREMENT)
        self.axis.set_zlim(-0.5, 0.5)

        plt.show()

    def _create_triangular_surface(self, x, y, z, _color='b', _antialiased=True, _alpha=1.0):
        return self.axis.plot_trisurf(x, y, z, color=_color, antialiased=_antialiased, alpha=_alpha, edgecolor='black')
