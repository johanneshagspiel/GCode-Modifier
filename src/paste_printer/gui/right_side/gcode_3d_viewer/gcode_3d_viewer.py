import matplotlib.pyplot as plt
import open3d as o3d

from open3d.cpu.pybind.geometry import LineSet
from open3d.cpu.pybind.utility import Vector3dVector, Vector2iVector
from open3d.cpu.pybind.visualization import draw_geometries


class Gcode_3D_Viewer():

    def __init__(self):
        None

    def test_matplotlib(self, layer_list):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        counter = 0

        for layer in layer_list:
            for x, y, z, color in zip(layer.x_data, layer.y_data, layer.z_data, layer.color_data):
                if counter != 0:
                    ax.plot3D(x, y, z, color)
                counter += 1
        plt.show()

    def show_with_open3D(self, layer_list):

        points = []
        lines = []
        counter = 0

        for layer in layer_list:
            for x, y, z in zip(layer.x_data, layer.y_data, layer.z_data):
                if counter != 0:
                    points.append([x[0], y[0], z[0]])
                    lines.append((counter - 1, counter))
                counter += 1

        line_set = LineSet()
        line_set.points = Vector3dVector(points)
        line_set.lines = Vector2iVector(lines)

        draw_geometries([line_set], width=720, height=720)
