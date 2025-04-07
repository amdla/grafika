# renderer.py
import math
import tkinter as tk
from bsp import build_bsp, dot, vector_sub
from cubes import cube_data  # Your existing 3D objects


class Renderer:
    def __init__(self, root, camera):
        self.root = root
        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack()

        self.camera = camera

        # Key bindings for camera movement
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

        # Initialize BSP
        self.polygons = cube_data  # Assuming cube_data is a list of polygons (your 3D objects)
        self.bsp_tree = build_bsp(self.polygons, self.camera.pos, self.camera.get_forward_vector())

        self.render()

    def draw_controls(self):
        control_info = """
        Controls:
        W/S - Move forward/backward
        A/D - Strafe left/right
        Q/E - Move up/down
        F/G - Roll clockwise/counter-clockwise
        Arrows - Look around
        """
        self.canvas.create_rectangle(10, 10, 450, 140, fill="#202020", outline="#404040")
        self.controls_text = self.canvas.create_text(
            20, 20, anchor="nw",
            text=control_info,
            fill="white",
            font=("Consolas", 10)
        )

    def project_point(self, point):
        # Project 3D points to 2D using perspective projection
        tx = point[0] - self.camera.pos[0]
        ty = point[1] - self.camera.pos[1]
        tz = point[2] - self.camera.pos[2]

        cos_y = math.cos(self.camera.yaw)
        sin_y = math.sin(self.camera.yaw)
        rx = tx * cos_y + ty * sin_y
        ry = -tx * sin_y + ty * cos_y
        rz = tz

        cos_p = math.cos(self.camera.pitch)
        sin_p = math.sin(self.camera.pitch)
        ry, rz = ry * cos_p - rz * sin_p, ry * sin_p + rz * cos_p

        cos_r = math.cos(self.camera.roll)
        sin_r = math.sin(self.camera.roll)
        rx_final = rx * cos_r - ry * sin_r
        ry_final = rx * sin_r + ry * cos_r

        if rz <= 0:
            return None  # Behind the camera

        f = 500.0
        scale = f / rz
        sx = 400 + rx_final * scale
        sy = 300 - ry_final * scale
        return sx, sy

    def render_bsp(self, bsp_node):
        if not bsp_node:
            return

        # Check if the current node is in front or behind the camera
        dot_product = dot(vector_sub(bsp_node.polygon[0], self.camera.pos), self.camera.get_forward_vector())

        if dot_product > 0:
            # Render the front part first (closer polygons)
            self.render_bsp(bsp_node.front)
            self.render_polygon(bsp_node.polygon)
            self.render_bsp(bsp_node.back)
        else:
            # Render the back part first (further polygons)
            self.render_bsp(bsp_node.back)
            self.render_polygon(bsp_node.polygon)
            self.render_bsp(bsp_node.front)

    def render_polygon(self, polygon):
        # Convert polygon to 2D points and render it on the canvas
        projected_points = []
        for vert in polygon:
            p = self.project_point(vert)
            if p:
                projected_points.append(p)

        if len(projected_points) > 2:
            self.canvas.create_polygon(projected_points, outline="black", fill="gray")

    def render(self):
        self.canvas.delete('all')
        self.render_bsp(self.bsp_tree)
        self.draw_controls()

    # Movement methods
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
