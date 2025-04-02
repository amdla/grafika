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

    def get_forward(self):
        """
        Basic forward vector from yaw/pitch.
        NOTE: In this sample, forward is determined by:
          fx = cos(pitch)*sin(yaw)
          fy = cos(pitch)*(-cos(yaw))    # minus sign means +yaw turns left
          fz = sin(pitch)
        """
        fx = math.cos(self.pitch) * math.sin(self.yaw)
        fy = math.cos(self.pitch) * (-math.cos(self.yaw))
        fz = math.sin(self.pitch)
        return (fx, fy, fz)

    def get_right(self):
        """
        A simple 'right' vector by taking the camera's forward
        and crossing with a global up (0,0,1). Then normalize.
        """
        f = self.get_forward()
        up = (0, 0, 1)
        r = cross(f, up)
        length = math.sqrt(r[0] * r[0] + r[1] * r[1] + r[2] * r[2])
        if length < 1e-9:
            return (0, 0, 0)
        return (r[0] / length, r[1] / length, r[2] / length)

    def get_up_direction(self):
        """
        If we wanted a true camera 'up', we'd do cross(right, forward),
        but for vertical movement let's keep world up (0,0,1).
        """
        return (0, 0, 1)
