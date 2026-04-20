import numpy as np
from math import pi
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
import os

def rad_to_grad(rad):
    return rad * 200 / pi

def grad_to_rad(grad):
    return grad * pi / 200

def rad_to_degrees(rad):
    return rad * 180 / pi

class Point:
    def __init__(self,name,x,y,sigmax2,sigmay2,sigmaxy):
        self.name = name
        self.x = x
        self.y = y
        self.sigmax2 = sigmax2
        self.sigmay2 = sigmay2
        self.sigmaxy = sigmaxy

    def calculate_error_ellipse(self):
        self.max_ax = math.sqrt(1/2 * ((self.sigmax2+self.sigmay2) + math.sqrt((self.sigmax2-self.sigmay2)**2 + 4*self.sigmaxy**2)))
        self.min_ax = math.sqrt(1/2 * ((self.sigmax2+self.sigmay2) - math.sqrt((self.sigmax2-self.sigmay2)**2 + 4*self.sigmaxy**2)))
        self.angle_rad = 1/2 * math.atan(2 * self.sigmaxy / (self.sigmax2 - self.sigmay2))

        if math.sqrt(self.sigmax2) > math.sqrt(self.sigmay2):
            if self.sigmaxy > 0:
                self.angle_rad = self.angle_rad
            else:
                self.angle_rad = self.angle_rad + pi
                
        elif math.sqrt(self.sigmax2) < math.sqrt(self.sigmay2):
            self.angle_rad  = self.angle_rad  + pi/2

        else:
            if self.sigmaxy > 0:
                self.angle_rad = grad_to_rad(50)
            else:
                self.angle_rad  = grad_to_rad(150)

        return self.angle_rad, self.max_ax, self.min_ax

    def calculate_rotation_matrix(self):
        return np.array([[math.cos(self.angle_rad) , -math.sin(self.angle_rad)],[math.sin(self.angle_rad) , math.cos(self.angle_rad)]])

    def calculate_rotated_error_ellipse(self):
        t = np.linspace(0, 2 * pi, 100)

        ellipse = np.array([
            self.max_ax * np.cos(t),
            self.min_ax * np.sin(t)
        ])  # shape (2, 100)

        R = self.calculate_rotation_matrix()
        rotated_ellipse = np.dot(R, ellipse)

        return rotated_ellipse

def Calculation(point_names, point_coordinates, point_sigmas):
    point_x = []
    point_y = []
    sigmax2 = []
    sigmay2 = []
    sigmaxy = []
    points = []

    number_of_points = len(point_names)

    for i in range(number_of_points):
        point_x.append(point_coordinates[i][0])
        point_y.append(point_coordinates[i][1])
        sigmax2.append(point_sigmas[i][0])
        sigmay2.append(point_sigmas[i][1])
        sigmaxy.append(point_sigmas[i][2])

    for point_info in zip(point_names, point_x, point_y, sigmax2, sigmay2, sigmaxy):
        point = Point(point_info[0], point_info[1], point_info[2], point_info[3], point_info[4], point_info[5])
        points.append(point)

    point_name = []
    max_axes = []
    min_axes = []
    angle_rot_rad = []
    angle_rot_grad = []

    for point_object in points:
        fig, ax = plt.subplots()
        angle_rot, max_ax, min_ax = point_object.calculate_error_ellipse()
        final_ellipse = point_object.calculate_rotated_error_ellipse()

        point_name.append(point_object.name)
        max_axes.append(max_ax)
        min_axes.append(min_ax)
        angle_rot_rad.append(angle_rot)
        angle_rot_grad.append(rad_to_grad(angle_rot))

        plt.plot(point_object.x, point_object.y, 'o')
        plt.grid(color='lightgray', linestyle='--')

        plt.plot(
            point_object.x + final_ellipse[0, :],
            point_object.y + final_ellipse[1, :]
        )

        ax.annotate(
            point_object.name,
            (point_object.x, point_object.y),
            xytext=(5, 5),
            textcoords='offset points'
        )

        slope = np.tan(angle_rot)
        ax.axline((point_object.x, point_object.y), slope=slope, color='green')
        ax.axline((point_object.x, point_object.y), slope=0, color='blue', linestyle='--')

        #print(point_object.name)
        #print(round(angle_rot, 4), round(max_ax, 3), round(min_ax, 3), round(rad_to_grad(angle_rot), 4))
        plt.gca().set_aspect('equal', adjustable='box')

        ax.set_aspect('equal', adjustable='box')

        angle_deg = rad_to_degrees(angle_rot)
        if angle_deg < 0:
            angle_deg += 180

        arc_radius = 0.4 * min_ax
        angle_arc = Arc(
            (point_object.x, point_object.y),
            2 * arc_radius,
            2 * arc_radius,
            angle=0,
            theta1=0,
            theta2=angle_deg,
            color='blue',
            linestyle='--')

        ax = plt.gca()
        ax.add_patch(angle_arc)

        # text outside
        fig.text(
            0.60, 0.90,
            "θ = " + str(round(rad_to_grad(angle_rot), 4)) + " grad",
            color='blue'
        )
        fig.text(
            0.20, 0.95,
            "Major axis = " + str(round(max_ax, 3)) + " m"
        )
        fig.text(
            0.60, 0.95,
            "Minor axis = " + str(round(min_ax, 3)) + " m"
        )

        plt.text(point_object.x + 0.020, point_object.y + 0.020, "θ", color='blue')
        plt.grid(color='lightgray', linestyle='--')

        plt.ylabel('Y')
        plt.xlabel('X')
        folder = 'Graph_Database'

        if not os.path.exists(folder):
            os.makedirs(folder)

        filename = f'Ellipse_{point_object.name}.png'
        filepath = os.path.join(folder, filename)

        plt.savefig(filepath)
        plt.close(fig)
        # plt.show()

    return point_name, max_axes, min_axes, angle_rot_rad, angle_rot_grad



