import math
from bsp import cross


class Camera:
    def __init__(self):
        self.pos = [1, 11, 5]
        self.yaw = math.radians(0)
        self.pitch = math.radians(-120)
        self.move_speed = 0.5
        self.rot_speed = math.radians(5)
        self.roll = 0

    def get_forward_vector(self):
        fx = math.cos(self.pitch) * math.sin(self.yaw)
        fy = math.cos(self.pitch) * (-math.cos(self.yaw))
        fz = math.sin(self.pitch)
        return (fx, fy, fz)

    def get_right_vector(self):
        f = self.get_forward_vector()
        up = (0, 0, 1)
        r = cross(f, up)
        length = math.sqrt(r[0] ** 2 + r[1] ** 2 + r[2] ** 2)
        if length < 1e-9:
            return (0, 0, 0)
        return (r[0] / length, r[1] / length, r[2] / length)

    def get_up_direction(self):
        return (0, 0, 1)
