import tkinter as tk
import math

from camera import Camera
from bsp import build_bsp, cube_faces, render_bsp


class App:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=800, height=600, bg="white")
        self.canvas.pack()

        self.camera = Camera()
        # Build the BSP tree once for the cube faces
        self.bsp_root = build_bsp(cube_faces)

        # Key bindings for movement/rotation
        root.bind("<w>", lambda e: self.move_forward())
        root.bind("<s>", lambda e: self.move_backward())
        root.bind("<Left>", lambda e: self.turn_left())
        root.bind("<Right>", lambda e: self.turn_right())
        root.bind("<Up>", lambda e: self.pitch_up())
        root.bind("<Down>", lambda e: self.pitch_down())

        # Additional keys for strafing, up/down, rolling
        root.bind("<a>", lambda e: self.move_left())
        root.bind("<d>", lambda e: self.move_right())
        root.bind("<q>", lambda e: self.move_up())
        root.bind("<e>", lambda e: self.move_down())
        root.bind("<f>", lambda e: self.roll_clockwise())
        root.bind("<g>", lambda e: self.roll_counter_clockwise())

        self.draw_controls_text()
        self.render()

    def draw_controls_text(self):
        info = (
            "Controls:\n"
            "W/S - Move forward/backward\n"
            "A/D - Strafe left/right\n"
            "Q/E - Move up/down\n"
            "F/G - Roll clockwise/counter-clockwise\n"
            "Arrows - Turn / Look around"
        )
        self.canvas.create_text(10, 10, anchor="nw", text=info, fill="black",
                                font=("Consolas", 10))

    def render(self):
        self.canvas.delete("all")
        self.draw_controls_text()
        # Traverse the BSP tree in back-to-front order from camera viewpoint
        render_bsp(self.bsp_root, self.camera, self.canvas, self.project_point)

    # -------------------------------------------------------------------------
    #            Projection: 3D -> 2D with camera transforms
    # -------------------------------------------------------------------------
    def project_point(self, point3d, camera, canvas_w, canvas_h):
        """
        Basic 3D -> 2D projection with rotation by camera yaw/pitch/roll
        and perspective.
        """
        # Translate relative to camera
        cx, cy, cz = camera.pos
        x, y, z = (point3d[0] - cx, point3d[1] - cy, point3d[2] - cz)

        # Yaw rotation (around Z)
        cos_y = math.cos(camera.yaw)
        sin_y = math.sin(camera.yaw)
        rx = x * cos_y - y * sin_y
        ry = x * sin_y + y * cos_y
        rz = z

        # Pitch rotation (around X)
        cos_p = math.cos(camera.pitch)
        sin_p = math.sin(camera.pitch)
        r2y = ry * cos_p - rz * sin_p
        r2z = ry * sin_p + rz * cos_p
        rx_final = rx
        ry_final = r2y
        rz_final = r2z

        # Roll rotation (around the forward axis)
        cos_r = math.cos(camera.roll)
        sin_r = math.sin(camera.roll)
        r3x = rx_final * cos_r - ry_final * sin_r
        r3y = rx_final * sin_r + ry_final * cos_r
        r3z = rz_final

        # Perspective
        if r3z <= 0:
            return None  # behind camera
        focal_length = 300
        scale = focal_length / r3z
        sx = (canvas_w / 2) + r3x * scale
        sy = (canvas_h / 2) - r3y * scale
        return (sx, sy)

    # -------------------------------------------------------------------------
    #                        Movement & Rotation
    # -------------------------------------------------------------------------
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

    def pitch_up(self):
        self.camera.pitch -= self.camera.rot_speed
        self.render()

    def pitch_down(self):
        self.camera.pitch += self.camera.rot_speed
        self.render()

    def roll_clockwise(self):
        self.camera.roll -= self.camera.rot_speed
        self.render()

    def roll_counter_clockwise(self):
        self.camera.roll += self.camera.rot_speed
        self.render()
