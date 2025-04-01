import math
import tkinter as tk

# 3D Data Structure (Cube edges) - Adjusted sizes and positions
cube_data = [
    # Cube 1 (0,0,0) with adjusted height
    ((0, 0, 0), (1, 0, 0)), ((1, 0, 0), (1, 0.5, 0)), ((1, 0.5, 0), (0, 0.5, 0)), ((0, 0.5, 0), (0, 0, 0)),
    ((0, 0, 1), (1, 0, 1)), ((1, 0, 1), (1, 0.5, 1)), ((1, 0.5, 1), (0, 0.5, 1)), ((0, 0.5, 1), (0, 0, 1)),
    ((0, 0, 0), (0, 0, 1)), ((1, 0, 0), (1, 0, 1)), ((1, 0.5, 0), (1, 0.5, 1)), ((0, 0.5, 0), (0, 0.5, 1)),

    # Cube 2 (2,0,0) with adjusted height
    ((2, 0, 0), (3, 0, 0)), ((3, 0, 0), (3, 0.5, 0)), ((3, 0.5, 0), (2, 0.5, 0)), ((2, 0.5, 0), (2, 0, 0)),
    ((2, 0, 1), (3, 0, 1)), ((3, 0, 1), (3, 0.5, 1)), ((3, 0.5, 1), (2, 0.5, 1)), ((2, 0.5, 1), (2, 0, 1)),
    ((2, 0, 0), (2, 0, 1)), ((3, 0, 0), (3, 0, 1)), ((3, 0.5, 0), (3, 0.5, 1)), ((2, 0.5, 0), (2, 0.5, 1)),

    # Cube 3 (0,2,0) with adjusted height
    ((0, 2, 0), (1, 2, 0)), ((1, 2, 0), (1, 2.5, 0)), ((1, 2.5, 0), (0, 2.5, 0)), ((0, 2.5, 0), (0, 2, 0)),
    ((0, 2, 1), (1, 2, 1)), ((1, 2, 1), (1, 2.5, 1)), ((1, 2.5, 1), (0, 2.5, 1)), ((0, 2.5, 1), (0, 2, 1)),
    ((0, 2, 0), (0, 2, 1)), ((1, 2, 0), (1, 2, 1)), ((1, 2.5, 0), (1, 2.5, 1)), ((0, 2.5, 0), (0, 2.5, 1)),

    # Cube 4 (2,2,0) with adjusted height
    ((2, 2, 0), (3, 2, 0)), ((3, 2, 0), (3, 2.5, 0)), ((3, 2.5, 0), (2, 2.5, 0)), ((2, 2.5, 0), (2, 2, 0)),
    ((2, 2, 1), (3, 2, 1)), ((3, 2, 1), (3, 2.5, 1)), ((3, 2.5, 1), (2, 2.5, 1)), ((2, 2.5, 1), (2, 2, 1)),
    ((2, 2, 0), (2, 2, 1)), ((3, 2, 0), (3, 2, 1)), ((3, 2.5, 0), (3, 2.5, 1)), ((2, 2.5, 0), (2, 2.5, 1)),
]


class Camera:
    def __init__(self):
        self.pos = [1, 9, 3]  # Closer position
        self.yaw = math.radians(0)  # Face southwest
        self.pitch = math.radians(-120)  # Look downward
        self.move_speed = 0.5
        self.rot_speed = math.radians(5)
        self.roll = 0  # NEW: Added roll parameter

    def get_forward_vector(self):
        return [
            math.cos(self.pitch) * math.cos(self.yaw),
            math.cos(self.pitch) * math.sin(self.yaw),
            math.sin(self.pitch)
        ]

    def get_right_vector(self):
        forward = self.get_forward_vector()
        # Compute right vector as up × forward
        right_x = forward[1]
        right_y = -forward[0]
        length = math.sqrt(right_x ** 2 + right_y ** 2)
        if length == 0:
            return [0, 0, 0]
        return [right_x / length, right_y / length, 0]


class Renderer:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack()
        self.camera = Camera()

        # Keybinds (updated F/G)
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
        self.root.bind('<f>', lambda e: self.roll_clockwise())  # Changed
        self.root.bind('<g>', lambda e: self.roll_counter_clockwise())  # Changed

        self.render()
        self.controls_text = None  # Reference to the text object

    def draw_controls(self):
        control_info = """
        Controls:
        W/S - Move forward/backward
        A/D - Strafe left/right
        Q/E - Move up/down
        F/G - Turn clockwise/counter-clockwise
        Arrows - Look around
        """

        # Draw semi-transparent background
        self.canvas.create_rectangle(
            10, 10, 450, 140,
            fill="#202020",
            outline="#404040"
        )

        # Draw text
        self.controls_text = self.canvas.create_text(
            20, 20,
            anchor="nw",
            text=control_info,
            fill="white",
            font=("Consolas", 10)
        )

    def project_point(self, point):
        """Project a 3D point (world space) onto the 2D canvas."""
        # 1) Translate into camera space
        tx = point[0] - self.camera.pos[0]
        ty = point[1] - self.camera.pos[1]
        tz = point[2] - self.camera.pos[2]

        # 2) Rotate around Z by yaw
        cos_y = math.cos(self.camera.yaw)
        sin_y = math.sin(self.camera.yaw)
        rx = tx * cos_y + ty * sin_y
        ry = -tx * sin_y + ty * cos_y
        rz = tz

        # 3) Rotate around X by pitch
        cos_p = math.cos(self.camera.pitch)
        sin_p = math.sin(self.camera.pitch)
        old_ry = ry
        old_rz = rz
        ry = old_ry * cos_p - old_rz * sin_p
        rz = old_ry * sin_p + old_rz * cos_p

        # NEW: Add roll rotation
        cos_r = math.cos(self.camera.roll)
        sin_r = math.sin(self.camera.roll)
        rx_final = rx * cos_r - ry * sin_r
        ry_final = rx * sin_r + ry * cos_r

        # Perspective projection using rolled coordinates
        if rz <= 0:
            return None

        f = 500.0
        scale = f / rz
        sx = 400 + rx_final * scale
        sy = 300 - ry_final * scale
        return sx, sy

        # NEW: Roll control methods

    def roll_clockwise(self):
        self.camera.roll -= self.camera.rot_speed
        self.render()

    def roll_counter_clockwise(self):
        self.camera.roll += self.camera.rot_speed
        self.render()

    def render(self):
        self.canvas.delete('all')

        # Draw ground "grid" points (just to visualize some reference)
        for gx in range(-5, 6):
            for gy in range(-5, 6):
                p = self.project_point((gx, gy, 0))
                if p:
                    self.canvas.create_oval(
                        p[0] - 1, p[1] - 1, p[0] + 1, p[1] + 1, fill='gray'
                    )

        # Draw cubes (lines)
        for (start, end) in cube_data:
            p1 = self.project_point(start)
            p2 = self.project_point(end)
            if p1 and p2:
                self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill='blue')

        self.draw_controls()

    # -------- Camera movement handlers ---------
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

    def turn_clockwise(self):
        self.camera.yaw -= self.camera.rot_speed
        self.render()

    def turn_counter_clockwise(self):
        self.camera.yaw += self.camera.rot_speed
        self.render()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("3D Viewer")
    app = Renderer(root)
    root.mainloop()
