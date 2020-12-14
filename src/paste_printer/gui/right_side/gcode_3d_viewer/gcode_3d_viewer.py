from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import numpy as np
import open3d as o3d

from open3d.cpu.pybind.geometry import LineSet
from open3d.cpu.pybind.utility import Vector3dVector, Vector2iVector
from open3d.cpu.pybind.visualization import draw_geometries


class Gcode_3D_Viewer():

    def __init__(self):
        None

    def test_matplotlib(self, layer_list):
        fig = plt.figure()
        ax = plt.axes(projection='3d')

        x_space = []
        y_space = []
        z_space = []

        for layer in layer_list:
            for x, y, z in zip(layer.x_data, layer.y_data, layer.z_data):
                x_space.append(x)
                y_space.append(y)
                z_space.append(z)

        ax.plot3D(x_space, y_space, z_space, 'gray')

        plt.show()

    def show_with_open3D(self, layer_list):

        points = []
        lines = []
        colors = []
        counter = 0

        for layer in layer_list:
            for x, y, z, color in zip(layer.x_data, layer.y_data, layer.z_data, layer.color_data):
                points.append([x, y, z])
                colors.append(color)
                if counter != 0:
                    lines.append([counter - 1, counter])
                counter += 1

        line_set = LineSet()
        line_set.points = Vector3dVector(points)
        line_set.lines = Vector2iVector(lines)

        #o3d.io.write_line_set("test.ply",line_set,write_ascii=True, print_progress=True)

        draw_geometries([line_set], width=720, height=720)
        #self.test_show_ply()
