import json
import tkinter as tk

import numpy as np


class CameraApp:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack()

        # config kamery
        self.position = np.array([3.0, 3.0, -10.0])
        self.move_speed = 0.5
        self.rotation_speed = 0.05
        self.focal_length = 500
        self.rotation_matrix = np.identity(3)

        # wczytaj obiekty
        with open('cube_data.json') as f:
            data = json.load(f)
        self.cube_data = [(tuple(p1), tuple(p2)) for p1, p2 in data]

        grid_center = np.array([4.0, 4.0, 4.0])
        direction = grid_center - self.position
        forward = direction / np.linalg.norm(direction)
        right = np.cross(forward, np.array([0, 1, 0])).astype(float)
        right /= np.linalg.norm(right)
        up = np.cross(right, forward)

        # macierz rotacji
        self.rotation_matrix = np.column_stack((right, up, -forward))
        yaw_180 = np.array([
            [-1, 0, 0],
            [0, 1, 0],
            [0, 0, -1]
        ])
        self.rotation_matrix = self.rotation_matrix @ yaw_180

        self.root.bind('<w>', lambda e: self.move_forward())
        self.root.bind('<s>', lambda e: self.move_backward())
        self.root.bind('<a>', lambda e: self.move_left())
        self.root.bind('<d>', lambda e: self.move_right())
        self.root.bind('<Up>', lambda e: self.look_up())
        self.root.bind('<Down>', lambda e: self.look_down())
        self.root.bind('<Left>', lambda e: self.turn_left())
        self.root.bind('<Right>', lambda e: self.turn_right())
        self.root.bind('<q>', lambda e: self.move_up())
        self.root.bind('<e>', lambda e: self.move_down())
        self.root.bind('<f>', lambda e: self.roll_clockwise())
        self.root.bind('<g>', lambda e: self.roll_counter_clockwise())
        self.root.bind('<h>', lambda e: self.zoom_in())
        self.root.bind('<j>', lambda e: self.zoom_out())

        self.draw_controls()
        self.redraw()

    # wektory
    def get_view_vectors(self):
        right = self.rotation_matrix[:, 0]
        up = self.rotation_matrix[:, 1]
        forward = -self.rotation_matrix[:, 2]
        return forward, right, up

    def move_forward(self):
        forward, _, _ = self.get_view_vectors()
        self.position -= forward * self.move_speed
        self.redraw()

    def move_backward(self):
        forward, _, _ = self.get_view_vectors()
        self.position += forward * self.move_speed
        self.redraw()

    def move_left(self):
        _, right, _ = self.get_view_vectors()
        self.position -= right * self.move_speed
        self.redraw()

    def move_right(self):
        _, right, _ = self.get_view_vectors()
        self.position += right * self.move_speed
        self.redraw()

    def move_up(self):
        _, _, up = self.get_view_vectors()
        self.position += up * self.move_speed
        self.redraw()

    def move_down(self):
        _, _, up = self.get_view_vectors()
        self.position -= up * self.move_speed
        self.redraw()

    def look_up(self):
        theta = self.rotation_speed
        c, s = np.cos(theta), np.sin(theta)
        delta_R = np.array([[1, 0, 0], [0, c, s], [0, -s, c]])
        self.rotation_matrix = self.rotation_matrix @ delta_R
        self.redraw()

    def look_down(self):
        theta = -self.rotation_speed
        c, s = np.cos(theta), np.sin(theta)
        delta_R = np.array([[1, 0, 0], [0, c, s], [0, -s, c]])
        self.rotation_matrix = self.rotation_matrix @ delta_R
        self.redraw()

    def turn_left(self):
        theta = self.rotation_speed
        c, s = np.cos(theta), np.sin(theta)
        delta_R = np.array([[c, 0, -s], [0, 1, 0], [s, 0, c]])
        self.rotation_matrix = self.rotation_matrix @ delta_R
        self.redraw()

    def turn_right(self):
        theta = -self.rotation_speed
        c, s = np.cos(theta), np.sin(theta)
        delta_R = np.array([[c, 0, -s], [0, 1, 0], [s, 0, c]])
        self.rotation_matrix = self.rotation_matrix @ delta_R
        self.redraw()

    def roll_clockwise(self):
        theta = -self.rotation_speed
        c, s = np.cos(theta), np.sin(theta)
        delta_R = np.array([[c, s, 0], [-s, c, 0], [0, 0, 1]])
        self.rotation_matrix = self.rotation_matrix @ delta_R
        self.redraw()

    def roll_counter_clockwise(self):
        theta = self.rotation_speed
        c, s = np.cos(theta), np.sin(theta)
        delta_R = np.array([[c, s, 0], [-s, c, 0], [0, 0, 1]])
        self.rotation_matrix = self.rotation_matrix @ delta_R
        self.redraw()

    def zoom_in(self):
        self.focal_length *= 1.1
        self.redraw()

    def zoom_out(self):
        self.focal_length /= 1.1
        self.redraw()

    def project_point(self, point):
        translated = np.array(point) - self.position
        rotated = self.rotation_matrix.T @ translated
        x, y, z = rotated
        if z <= 0:
            return None  # punkt za kamera
        x_proj = (x / z) * self.focal_length
        y_proj = (y / z) * self.focal_length
        return 400 + x_proj, 300 - y_proj

    def redraw(self):
        self.canvas.delete("all")
        for edge in self.cube_data:
            p1 = self.project_point(edge[0])
            p2 = self.project_point(edge[1])
            if p1 and p2:
                self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill='black')
        self.draw_controls()

    def draw_controls(self):
        controls = """Controls:
        W/S - Move forward/backward
        A/D - Strafe left/right
        Q/E - Move up/down
        F/G - Roll clockwise/counter
        Arrows - Look around
        H/J - Zoom in/out"""
        self.canvas.create_text(10, 10, text=controls, anchor='nw', fill='black')
