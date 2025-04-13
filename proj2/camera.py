import math

from bsp import cross


class Camera:
    def __init__(self):
        self.pos = [1, 11, 5]
        self.yaw = math.radians(0)
        self.pitch = math.radians(-120)
        self.roll = 0
        self.move_speed = 0.5
        self.rot_speed = math.radians(5)

    def get_forward_vector(self):
        fx = math.cos(self.pitch) * math.sin(self.yaw)
        fy = -math.cos(self.pitch) * math.cos(self.yaw)
        fz = math.sin(self.pitch)
        return (fx, fy, fz)

    def get_right_vector(self):
        forward = self.get_forward_vector()
        world_up = (0, 0, 1)
        right = cross(forward, world_up)
        length = math.sqrt(sum(x ** 2 for x in right))
        if length < 1e-9:
            return (0, 0, 0)
        right = (right[0] / length, right[1] / length, right[2] / length)

        # Apply roll rotation
        cr = math.cos(self.roll)
        sr = math.sin(self.roll)
        right_rolled = (
            right[0] * cr + forward[1] * right[2] * sr - forward[2] * right[1] * sr,
            right[1] * cr + forward[2] * right[0] * sr - forward[0] * right[2] * sr,
            right[2] * cr + forward[0] * right[1] * sr - forward[1] * right[0] * sr
        )
        return right_rolled

    def get_up_direction(self):
        right = self.get_right_vector()
        forward = self.get_forward_vector()
        up = cross(right, forward)
        length = math.sqrt(sum(x ** 2 for x in up))
        if length < 1e-9:
            return (0, 0, 0)
        return (up[0] / length, up[1] / length, up[2] / length)
