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
        """
        Wektor skierowany do przodu, pokazujący, w którą stronę kamera jest skierowana
        Kamera ma dwa kąty obrotu:

        Yaw – obrót prawo/lewo
        Pitch – obrót góra/dół

        W poziomie (XY) kierunek jest określony przez yaw:
        cos(yaw) - projekcja kierunku kamery na oś X.
        sin(yaw) - projekcja kierunku kamery na oś Y.

        W pionie (Z) kierunek jest określony przez pitch:
        cos(pitch) - projekcja kierunku na płaszczyznę XY.
        sin(pitch) - projekcja kierunku kamery na oś Z.

        Wynik mnożenia tych dwóch projekcji daje ostateczny trójwymiarowy kierunek kamery:

        X: cos(pitch) * cos(yaw)
        Y: cos(pitch) * sin(yaw)
        Z: sin(pitch)
        """
        return [
            math.cos(self.pitch) * math.cos(self.yaw),
            math.cos(self.pitch) * math.sin(self.yaw),
            math.sin(self.pitch)
        ]

    def get_right_vector(self):
        """
        Znormalnizowany wektor skierowany w prawo potrzebny do przesuwania na boki (wektor forward
        przekręcony o 90 stopni przez zamianę miejscami składowych X oraz Y i zmianę znaku jednej z nich)
        """
        forward = self.get_forward_vector()
        right_x = forward[1]
        right_y = -forward[0]
        length = math.sqrt(right_x ** 2 + right_y ** 2)
        if length == 0:
            return [0, 0, 0]
        return [right_x / length, right_y / length, 0]
