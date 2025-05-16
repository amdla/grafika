import json
import tkinter as tk

import numpy as np


class Plane:
    def __init__(self, point, normal):
        self.point = np.array(point)
        self.normal = np.array(normal)

        self.normal = self.normal / np.linalg.norm(self.normal)

    def classify_point(self, point):
        # Oblicz iloczyn skalarny zeby wiedziec z ktorej strony plaszczyzny jest punkt
        v = np.array(point) - self.point
        dot = np.dot(v, self.normal)

        if dot > 1e-6:
            return "FRONT"
        elif dot < -1e-6:
            return "BACK"
        else:
            return "COPLANAR"

    def classify_polygon(self, polygon):
        # Gdzie lezy wielokat wzgledem plaszczyzny
        front_count = 0
        back_count = 0

        for point in polygon:
            classification = self.classify_point(point)
            if classification == "FRONT":
                front_count += 1
            elif classification == "BACK":
                back_count += 1

        if front_count > 0 and back_count == 0:
            return "FRONT"
        elif back_count > 0 and front_count == 0:
            return "BACK"
        elif front_count == 0 and back_count == 0:
            return "COPLANAR"
        else:
            return "SPANNING"

    def split_polygon(self, polygon):
        # Podziel wielokat przez plaszczyzne
        # Zwraca front_poly, back_poly
        front_points = []
        back_points = []

        # Dodaj kazdy punkt do odpowiedniej listy
        for i in range(len(polygon)):
            current = polygon[i]
            next_point = polygon[(i + 1) % len(polygon)]

            current_classification = self.classify_point(current)
            next_classification = self.classify_point(next_point)

            if current_classification == "FRONT" or current_classification == "COPLANAR":
                front_points.append(current)
            if current_classification == "BACK" or current_classification == "COPLANAR":
                back_points.append(current)

            # Jesli krawedz przecina plaszczyzne, stworz punkt przeciecia i dodaj do obu stron
            if (current_classification == "FRONT" and next_classification == "BACK") or \
                    (current_classification == "BACK" and next_classification == "FRONT"):
                current_array = np.array(current)
                next_array = np.array(next_point)
                direction = next_array - current_array

                # Oblicz punkt przeciecia
                t = np.dot(self.point - current_array, self.normal) / np.dot(direction, self.normal)
                intersection = current_array + t * direction

                # Dodaj przeciecie do obu stron
                front_points.append(tuple(intersection))
                back_points.append(tuple(intersection))

        return front_points if len(front_points) >= 3 else None, back_points if len(back_points) >= 3 else None


class BSPNode:
    def __init__(self, polygons=None):
        self.plane = None
        self.front = None
        self.back = None
        self.polygons = []

        if polygons:
            self.build(polygons)

    def build(self, polygons):
        if not polygons:
            return

        # Wez pierwszy wielokat zeby zdefiniowac plaszczyzne podzialu
        first_poly = polygons[0]
        # Wez trzy punkty z wielokata, zeby ogarnac plaszczyzne
        p1, p2, p3 = first_poly[0], first_poly[1], first_poly[2]

        # Oblicz wektor normalny przez iloczyn wektorowy
        v1 = np.array(p2) - np.array(p1)
        v2 = np.array(p3) - np.array(p1)
        normal = np.cross(v1, v2)

        # Stworz plaszczyzne podzialu
        self.plane = Plane(p1, normal)

        # Podziel wielokaty na front, back i coplanar
        front_list = []
        back_list = []

        for poly in polygons:
            classification = self.plane.classify_polygon(poly)

            if classification == "FRONT":
                front_list.append(poly)
            elif classification == "BACK":
                back_list.append(poly)
            elif classification == "COPLANAR":
                # Dodaj do wielokatow tego wezla
                self.polygons.append(poly)
            elif classification == "SPANNING":
                # Podziel wielokat i dodaj do obu stron
                front_poly, back_poly = self.plane.split_polygon(poly)
                if front_poly:
                    front_list.append(front_poly)
                if back_poly:
                    back_list.append(back_poly)

        # Zbuduj rekurencyjnie poddrzewa
        if front_list:
            self.front = BSPNode(front_list)
        if back_list:
            self.back = BSPNode(back_list)

    def get_visible_polygons(self, camera_position):
        result = []

        # Jesli nie ma plaszczyzny, to jest lisc w drzewie
        if not self.plane:
            return self.polygons

        # Sprawdz po ktorej stronie plaszczyzny jest kamera
        camera_side = self.plane.classify_point(camera_position)

        # Przejdz drzewo w odpowiedniej kolejnosci w zaleznosci od pozycji kamery
        if camera_side == "FRONT" or camera_side == "COPLANAR":
            # Kamera jest z przodu lub na plaszczyznie
            # Najpierw przerob tyl (dalej od kamery)
            if self.back:
                result.extend(self.back.get_visible_polygons(camera_position))

            # Dodaj wielokaty tego wezla
            result.extend(self.polygons)

            # Potem przerob przod (blizej kamery)
            if self.front:
                result.extend(self.front.get_visible_polygons(camera_position))
        else:
            # Kamera jest z tylu
            # Przerob przod najpierw
            if self.front:
                result.extend(self.front.get_visible_polygons(camera_position))

            # Dodaj wielokaty tego wezla
            result.extend(self.polygons)

            # Potem przerob tyl
            if self.back:
                result.extend(self.back.get_visible_polygons(camera_position))

        return result


class CameraApp:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack()

        # config kamery
        self.position = np.array([3.0, 3.0, -10.0])
        self.move_speed = 0.5
        self.rotation_speed = 0.05
        self.focal_length = 500
        self.rotation_matrix = np.identity(3)

        with open('cube_polygons.json') as f:
            self.polygons = json.load(f)
            self.polygons = [[tuple(point) for point in polygon] for polygon in self.polygons]

        # Wczytaj krawedzie do wyswietlania bez BSP
        with open('cube_data.json') as f:
            data = json.load(f)
        self.cube_data = [(tuple(p1), tuple(p2)) for p1, p2 in data]

        # Zbuduj drzewo BSP
        self.bsp_tree = BSPNode(self.polygons)

        grid_center = np.array([4.0, 4.0, 4.0])
        direction = grid_center - self.position
        forward = direction / np.linalg.norm(direction)
        right = np.cross(forward, np.array([0, 1, 0])).astype(float)
        right /= np.linalg.norm(right)
        up = np.cross(right, forward)

        # macierz rotacji
        self.rotation_matrix = np.column_stack((right, up, -forward))
        yaw_180 = np.array([
            [-1, 0, 0],
            [0, 1, 0],
            [0, 0, -1]
        ])
        self.rotation_matrix = self.rotation_matrix @ yaw_180

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
        self.root.bind('<h>', lambda e: self.zoom_in())
        self.root.bind('<j>', lambda e: self.zoom_out())
        self.root.bind('<b>', lambda e: self.toggle_bsp())

        self.use_bsp = True
        self.draw_controls()
        self.redraw()

    def toggle_bsp(self):
        self.use_bsp = not self.use_bsp
        self.redraw()

    def get_view_vectors(self):
        right = self.rotation_matrix[:, 0]
        up = self.rotation_matrix[:, 1]
        forward = -self.rotation_matrix[:, 2]
        return forward, right, up

    def move_forward(self):
        forward, _, _ = self.get_view_vectors()
        self.position -= forward * self.move_speed
        self.redraw()

    def move_backward(self):
        forward, _, _ = self.get_view_vectors()
        self.position += forward * self.move_speed
        self.redraw()

    def move_left(self):
        _, right, _ = self.get_view_vectors()
        self.position -= right * self.move_speed
        self.redraw()

    def move_right(self):
        _, right, _ = self.get_view_vectors()
        self.position += right * self.move_speed
        self.redraw()

    def move_up(self):
        _, _, up = self.get_view_vectors()
        self.position += up * self.move_speed
        self.redraw()

    def move_down(self):
        _, _, up = self.get_view_vectors()
        self.position -= up * self.move_speed
        self.redraw()

    def look_up(self):
        theta = self.rotation_speed
        c, s = np.cos(theta), np.sin(theta)
        delta_R = np.array([[1, 0, 0], [0, c, s], [0, -s, c]])
        self.rotation_matrix = self.rotation_matrix @ delta_R
        self.redraw()

    def look_down(self):
        theta = -self.rotation_speed
        c, s = np.cos(theta), np.sin(theta)
        delta_R = np.array([[1, 0, 0], [0, c, s], [0, -s, c]])
        self.rotation_matrix = self.rotation_matrix @ delta_R
        self.redraw()

    def turn_left(self):
        theta = self.rotation_speed
        c, s = np.cos(theta), np.sin(theta)
        delta_R = np.array([[c, 0, -s], [0, 1, 0], [s, 0, c]])
        self.rotation_matrix = self.rotation_matrix @ delta_R
        self.redraw()

    def turn_right(self):
        theta = -self.rotation_speed
        c, s = np.cos(theta), np.sin(theta)
        delta_R = np.array([[c, 0, -s], [0, 1, 0], [s, 0, c]])
        self.rotation_matrix = self.rotation_matrix @ delta_R
        self.redraw()

    def roll_clockwise(self):
        theta = -self.rotation_speed
        c, s = np.cos(theta), np.sin(theta)
        delta_R = np.array([[c, s, 0], [-s, c, 0], [0, 0, 1]])
        self.rotation_matrix = self.rotation_matrix @ delta_R
        self.redraw()

    def roll_counter_clockwise(self):
        theta = self.rotation_speed
        c, s = np.cos(theta), np.sin(theta)
        delta_R = np.array([[c, s, 0], [-s, c, 0], [0, 0, 1]])
        self.rotation_matrix = self.rotation_matrix @ delta_R
        self.redraw()

    def zoom_in(self):
        self.focal_length *= 1.1
        self.redraw()

    def zoom_out(self):
        self.focal_length /= 1.1
        self.redraw()

    def project_point(self, point):
        translated = np.array(point) - self.position
        rotated = self.rotation_matrix.T @ translated
        x, y, z = rotated
        if z <= 0:
            return None  # punkt za kamera
        x_proj = (x / z) * self.focal_length
        y_proj = (y / z) * self.focal_length
        return 400 + x_proj, 300 - y_proj

    def calculate_polygon_normal(self, polygon):
        if len(polygon) < 3:
            return np.array([0, 0, 0])

        # Oblicz wektor normalny dla wielokata
        v1 = np.array(polygon[1]) - np.array(polygon[0])
        v2 = np.array(polygon[2]) - np.array(polygon[0])
        normal = np.cross(v1, v2)

        return normal / np.linalg.norm(normal) if np.linalg.norm(normal) > 0 else normal

    def is_polygon_facing_camera(self, polygon):
        normal = self.calculate_polygon_normal(polygon)
        centroid = np.mean([np.array(p) for p in polygon], axis=0)
        view_vector = centroid - self.position

        # Jesli iloczyn skalarny jest ujemny, wielokat jest skierowany w strone kamery
        return np.dot(normal, view_vector) < 0

    def redraw(self):
        self.canvas.delete("all")

        if self.use_bsp:
            # Uzyj drzewa BSP do eliminacji powierzchni zaslonietych
            visible_polygons = self.bsp_tree.get_visible_polygons(tuple(self.position))

            # Narysuj widoczne wielokaty
            for poly in visible_polygons:
                # Sprawdz, czy wielokat jest skierowany w strone kamery - inaczej go nie rysuj
                if not self.is_polygon_facing_camera(poly):
                    continue

                points_2d = []
                valid = True

                for point in poly:
                    proj = self.project_point(point)
                    if not proj:
                        valid = False
                        break
                    points_2d.append(proj)

                if valid and len(points_2d) >= 3:
                    flat_points = [coord for point in points_2d for coord in point]

                    gray_value = 200

                    color = f'#{gray_value:02x}{gray_value:02x}{gray_value:02x}'

                    # Renderuj tylko w trybie solid - pelne wielokaty
                    self.canvas.create_polygon(flat_points, fill=color, outline='black')
        else:
            # krawedzie bez BSP - tylko linie
            for edge in self.cube_data:
                p1 = self.project_point(edge[0])
                p2 = self.project_point(edge[1])
                if p1 and p2:
                    self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill='black')

        self.draw_controls()

    def draw_controls(self):
        controls = """Kontrolki:
        W/S - Ruch przód/tył
        A/D - Strafe lewo/prawo
        Q/E - Góra/dół
        F/G - Obrót w osi Z
        Strzałki - Rozglądanie
        H/J - Przybliż/oddal
        B - Przełącz BSP"""

        bsp_status = "BSP: ON" if self.use_bsp else "BSP: OFF"

        self.canvas.create_text(10, 10, text=controls, anchor='nw', fill='black')
        self.canvas.create_text(400, 10, text=bsp_status, anchor='n', fill='blue')


if __name__ == "__main__":
    root = tk.Tk()
    root.title("3D Camera with BSP Tree")
    app = CameraApp(root)
    root.mainloop()
