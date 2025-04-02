import math


class Camera:
    def __init__(self):
        self.pos = [1, 11, 5]
        self.yaw = math.radians(0)
        self.pitch = math.radians(-120)
        self.move_speed = 0.5
        self.rot_speed = math.radians(5)
        self.roll = 0

    def get_forward_vector(self):
        return [
            math.cos(self.pitch) * math.cos(self.yaw),
            math.cos(self.pitch) * math.sin(self.yaw),
            math.sin(self.pitch)
        ]

    def get_right_vector(self):
        forward = self.get_forward_vector()
        right_x = forward[1]
        right_y = -forward[0]
        length = math.sqrt(right_x ** 2 + right_y ** 2)
        if length == 0:
            return [0, 0, 0]
        return [right_x / length, right_y / length, 0]
