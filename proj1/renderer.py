import math
import tkinter as tk

from camera import Camera
from cubes import cube_data


class Renderer:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack()

        self.camera = Camera()

        # Key bindings
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

        self.controls_text = None
        self.render()

    def draw_controls(self):
        control_info = """
        Controls:
        W/S - Move forward/backward
        A/D - Strafe left/right
        Q/E - Move up/down
        F/G - Turn clockwise/counter-clockwise
        Arrows - Look around
        """
        # Create a semi-transparent background rectangle
        self.canvas.create_rectangle(10, 10, 450, 140, fill="#202020", outline="#404040")
        self.controls_text = self.canvas.create_text(
            20, 20, anchor="nw",
            text=control_info,
            fill="white",
            font=("Consolas", 10)
        )

    def project_point(self, point):
        # Translate points relative to camera
        tx = point[0] - self.camera.pos[0]
        ty = point[1] - self.camera.pos[1]
        tz = point[2] - self.camera.pos[2]

        # Yaw rotation
        cos_y = math.cos(self.camera.yaw)
        sin_y = math.sin(self.camera.yaw)
        rx = tx * cos_y + ty * sin_y
        ry = -tx * sin_y + ty * cos_y
        rz = tz

        # Pitch rotation
        cos_p = math.cos(self.camera.pitch)
        sin_p = math.sin(self.camera.pitch)
        ry, rz = ry * cos_p - rz * sin_p, ry * sin_p + rz * cos_p

        # Roll rotation
        cos_r = math.cos(self.camera.roll)
        sin_r = math.sin(self.camera.roll)
        rx_final = rx * cos_r - ry * sin_r
        ry_final = rx * sin_r + ry * cos_r

        # Simple perspective projection
        if rz <= 0:
            return None  # Behind the camera

        f = 500.0
        scale = f / rz
        sx = 400 + rx_final * scale
        sy = 300 - ry_final * scale
        return sx, sy

    def render(self):
        self.canvas.delete('all')

        # Draw a small grid for reference
        for gx in range(-5, 6):
            for gy in range(-5, 6):
                p = self.project_point((gx, gy, 0))
                if p:
                    self.canvas.create_oval(
                        p[0] - 1, p[1] - 1,
                        p[0] + 1, p[1] + 1,
                        fill='gray'
                    )

        # Draw the lines from cube_data
        for (start, end) in cube_data:
            p1 = self.project_point(start)
            p2 = self.project_point(end)
            if p1 and p2:
                self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill='black')

        self.draw_controls()

    # Movement and rotation methods
    def move_forward(self):
        dx = math.sin(self.camera.yaw) * self.camera.move_speed
        dy = -math.cos(self.camera.yaw) * self.camera.move_speed
        self.camera.pos[0] += dx
        self.camera.pos[1] += dy
        self.render()

    def move_backward(self):
        dx = math.sin(self.camera.yaw) * self.camera.move_speed
        dy = -math.cos(self.camera.yaw) * self.camera.move_speed
        self.camera.pos[0] -= dx
        self.camera.pos[1] -= dy
        self.render()

    def move_right(self):
        dx = math.cos(self.camera.yaw) * self.camera.move_speed
        dy = math.sin(self.camera.yaw) * self.camera.move_speed
        self.camera.pos[0] += dx
        self.camera.pos[1] += dy
        self.render()

    def move_left(self):
        dx = math.cos(self.camera.yaw) * self.camera.move_speed
        dy = math.sin(self.camera.yaw) * self.camera.move_speed
        self.camera.pos[0] -= dx
        self.camera.pos[1] -= dy
        self.render()

    def move_up(self):
        self.camera.pos[2] += self.camera.move_speed
        self.render()

    def move_down(self):
        self.camera.pos[2] -= self.camera.move_speed
        self.render()

    def turn_left(self):
        self.camera.yaw -= self.camera.rot_speed
        self.render()

    def turn_right(self):
        self.camera.yaw += self.camera.rot_speed
        self.render()

    def look_up(self):
        self.camera.pitch -= self.camera.rot_speed
        self.render()

    def look_down(self):
        self.camera.pitch += self.camera.rot_speed
        self.render()

    def roll_clockwise(self):
        self.camera.roll -= self.camera.rot_speed
        self.render()

    def roll_counter_clockwise(self):
        self.camera.roll += self.camera.rot_speed
        self.render()
