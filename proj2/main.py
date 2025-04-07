import tkinter as tk
import math
from cubes import cube_faces

class Main:
    def __init__(self, root):
        self.root = root
        self.camera = Camera()
        self.bsp_root = build_bsp(cube_faces)
        self.renderer = Renderer(root, self.camera, self.bsp_root)

        self.bind_keys()

        self.renderer.render()

    def bind_keys(self):
        root = self.root
        root.bind("<w>", lambda e: self.move_forward())
        root.bind("<s>", lambda e: self.move_backward())
        root.bind("<Left>", lambda e: self.turn_left())
        root.bind("<Right>", lambda e: self.turn_right())
        root.bind("<Up>", lambda e: self.pitch_up())
        root.bind("<Down>", lambda e: self.pitch_down())
        root.bind("<a>", lambda e: self.move_left())
        root.bind("<d>", lambda e: self.move_right())
        root.bind("<q>", lambda e: self.move_up())
        root.bind("<e>", lambda e: self.move_down())
        root.bind("<f>", lambda e: self.roll_clockwise())
        root.bind("<g>", lambda e: self.roll_counter_clockwise())

    def move_forward(self):
        dx = math.sin(self.camera.yaw) * self.camera.move_speed
        dy = -math.cos(self.camera.yaw) * self.camera.move_speed
        self.camera.pos[0] += dx
        self.camera.pos[1] += dy
        self.renderer.render()

    def move_backward(self):
        dx = math.sin(self.camera.yaw) * self.camera.move_speed
        dy = -math.cos(self.camera.yaw) * self.camera.move_speed
        self.camera.pos[0] -= dx
        self.camera.pos[1] -= dy
        self.renderer.render()

    def move_right(self):
        dx = math.cos(self.camera.yaw) * self.camera.move_speed
        dy = math.sin(self.camera.yaw) * self.camera.move_speed
        self.camera.pos[0] += dx
        self.camera.pos[1] += dy
        self.renderer.render()

    def move_left(self):
        dx = math.cos(self.camera.yaw) * self.camera.move_speed
        dy = math.sin(self.camera.yaw) * self.camera.move_speed
        self.camera.pos[0] -= dx
        self.camera.pos[1] -= dy
        self.renderer.render()

    def move_up(self):
        self.camera.pos[2] += self.camera.move_speed
        self.renderer.render()

    def move_down(self):
        self.camera.pos[2] -= self.camera.move_speed
        self.renderer.render()

    def turn_left(self):
        self.camera.yaw -= self.camera.rot_speed
        self.renderer.render()

    def turn_right(self):
        self.camera.yaw += self.camera.rot_speed
        self.renderer.render()

    def pitch_up(self):
        self.camera.pitch -= self.camera.rot_speed
        self.renderer.render()

    def pitch_down(self):
        self.camera.pitch += self.camera.rot_speed
        self.renderer.render()

    def roll_clockwise(self):
        self.camera.roll -= self.camera.rot_speed
        self.renderer.render()

    def roll_counter_clockwise(self):
        self.camera.roll += self.camera.rot_speed
        self.renderer.render()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("BSP Tree Hidden-Surface Example with Extended Movement")
    app = Main(root)
    root.mainloop()
