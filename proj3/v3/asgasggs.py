# Kompletna implementacja z poprawionym modelem Phonga

import numpy as np
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# Klasa reprezentująca punkt w przestrzeni 3D
class Point3D:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def normalize(self):
        length = math.sqrt(self.x**2 + self.y**2 + self.z**2)
        if length > 0:
            self.x /= length
            self.y /= length
            self.z /= length
        return self

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

# Klasa reprezentująca kolor RGB
class Color:
    def __init__(self, r=1.0, g=1.0, b=1.0):
        self.r = r
        self.g = g
        self.b = b

    def multiply(self, scalar):
        return Color(self.r * scalar, self.g * scalar, self.b * scalar)

    def multiply_color(self, other_color):
        return Color(self.r * other_color.r, self.g * other_color.g, self.b * other_color.b)

    def add(self, other):
        return Color(
            min(1.0, self.r + other.r),
            min(1.0, self.g + other.g),
            min(1.0, self.b + other.b)
        )

# Klasa reprezentująca źródło światła
class Light:
    def __init__(self, position, color=Color(1.0, 1.0, 1.0), intensity=1.0):
        self.position = position
        self.color = color
        self.intensity = intensity

# Klasa reprezentująca materiał
class Material:
    def __init__(self, name, ambient_color, diffuse_color, specular_color, shininess):
        self.name = name
        self.ambient = ambient_color   # Kolor ambient (otoczenia)
        self.diffuse = diffuse_color   # Kolor diffuse (rozproszenia)
        self.specular = specular_color # Kolor specular (kierunkowy)
        self.shininess = shininess     # Połysk (wyższy = ostrzejsze odbicie)

# Materiały predefiniowane z poprawnymi właściwościami
MATERIALS = {
    "wypolerowane_drewno": Material(
        "Wypolerowane Drewno",
        ambient_color=Color(0.1, 0.05, 0.02),  # Ciemnobrązowy ambient
        diffuse_color=Color(0.6, 0.3, 0.1),    # Brązowy diffuse
        specular_color=Color(0.3, 0.3, 0.2),   # Lekko żółtawy specular
        shininess=15
    ),
    "dobry_plastik": Material(
        "Dobry Plastik",
        ambient_color=Color(0.05, 0.1, 0.15),  # Lekko niebieskawy ambient
        diffuse_color=Color(0.2, 0.5, 0.7),    # Niebieski diffuse
        specular_color=Color(0.8, 0.8, 0.8),   # Białawy specular
        shininess=40
    ),
    "zloto": Material(
        "Złoto",
        ambient_color=Color(0.24, 0.20, 0.075),  # Ciemne złoto ambient
        diffuse_color=Color(0.75, 0.61, 0.23),   # Złoty diffuse
        specular_color=Color(1.0, 0.9, 0.4),     # Intensywnie złoty specular
        shininess=128
    )
}

# Funkcja implementująca model odbicia Phonga z komponentami RGB
def phong_reflection(point, normal, view_dir, material, lights):
    # Inicjalizacja koloru wynikowego
    result_color = Color(0, 0, 0)

    # Składowa ambient (otoczenia)
    ambient = material.ambient.multiply_color(Color(0.2, 0.2, 0.2))  # Globalne oświetlenie ambient
    result_color = ambient

    for light in lights:
        # Wektor od punktu do źródła światła
        light_dir = Point3D(
            light.position.x - point.x,
            light.position.y - point.y,
            light.position.z - point.z
        ).normalize()

        # Kąt między normalną a kierunkiem światła
        dot_product = normal.dot(light_dir)

        # Składowa diffuse (rozproszona)
        if dot_product > 0:
            # Obliczamy intensywność
            diffuse_intensity = dot_product * light.intensity
            # Kolor diffuse to iloczyn koloru światła i koloru diffuse materiału, przemnożony przez intensywność
            diffuse = light.color.multiply_color(material.diffuse).multiply(diffuse_intensity)
            result_color = result_color.add(diffuse)

        # Składowa specular (kierunkowa)
        if dot_product > 0:  # Specular obliczamy tylko dla powierzchni oświetlonych
            # Obliczenie wektora odbicia światła
            reflect_dir = Point3D(
                2 * dot_product * normal.x - light_dir.x,
                2 * dot_product * normal.y - light_dir.y,
                2 * dot_product * normal.z - light_dir.z
            ).normalize()

            # Obliczenie intensywności odbicia kierunkowego
            spec_angle = max(0, reflect_dir.dot(view_dir))
            if spec_angle > 0:
                # Intensywność zależy od kąta i współczynnika połysku
                spec_intensity = pow(spec_angle, material.shininess) * light.intensity
                # Kolor specular to iloczyn koloru światła i koloru specular materiału
                specular = light.color.multiply_color(material.specular).multiply(spec_intensity)
                result_color = result_color.add(specular)

    return result_color

# Funkcja generująca siatkę kuli
def generate_sphere(radius, resolution):
    vertices = []
    normals = []

    for i in range(resolution + 1):
        theta = i * math.pi / resolution
        sin_theta = math.sin(theta)
        cos_theta = math.cos(theta)

        for j in range(resolution * 2 + 1):
            phi = j * 2 * math.pi / (resolution * 2)
            sin_phi = math.sin(phi)
            cos_phi = math.cos(phi)

            x = radius * sin_theta * cos_phi
            y = radius * sin_theta * sin_phi
            z = radius * cos_theta

            vertex = Point3D(x, y, z)
            normal = Point3D(x, y, z).normalize()

            vertices.append(vertex)
            normals.append(normal)

    # Generowanie trójkątów (indeksy)
    indices = []
    for i in range(resolution):
        for j in range(resolution * 2):
            first = i * (resolution * 2 + 1) + j
            second = first + (resolution * 2 + 1)
            third = first + 1
            fourth = second + 1

            # Pierwszy trójkąt
            indices.append((first, second, third))
            # Drugi trójkąt
            indices.append((second, fourth, third))

    return vertices, normals, indices

def main():
    # Inicjalizacja Pygame i OpenGL
    pygame.init()
    display = (1920, 1080)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Model odbicia Phonga - Interaktywna aplikacja")

    # Ustawienia OpenGL
    glClearColor(0.05, 0.05, 0.1, 1)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0, 0, -5)

    # Generowanie kuli
    radius = 1.0
    resolution = 30
    vertices, normals, indices = generate_sphere(radius, resolution)

    # Ustawienia kamery
    camera_pos = Point3D(0, 0, 5)
    camera_rotation = [0, 0]  # [pitch, yaw]
    camera_speed = 0.4
    rotation_speed = 1.5

    # Tworzenie świateł
    light1 = Light(
        position=Point3D(3.0, 2.0, 3.0),
        color=Color(1.0, 0.9, 0.7),  # Ciepłe światło (żółtawe)
        intensity=0.8
    )

    light2 = Light(
        position=Point3D(-2.5, -1.0, 2.0),
        color=Color(0.6, 0.7, 1.0),  # Chłodne światło (niebieskawe)
        intensity=0.6
    )

    light3 = Light(
        position=Point3D(0.0, 3.0, 1.0),
        color=Color(1.0, 1.0, 1.0),  # Białe światło z góry
        intensity=1.0
    )

    light4 = Light(
        position=Point3D(0.0, -3.0, 0.0),
        color=Color(0.2, 0.9, 0.2),  # Zielone światło z dołu
        intensity=0.7
    )

    light5 = Light(
        position=Point3D(-2.0, 0.0, -3.0),
        color=Color(1.0, 0.2, 0.2),  # Czerwone światło z tyłu
        intensity=0.9
    )

    light6 = Light(
        position=Point3D(2.0, -2.0, -2.0),
        color=Color(0.8, 0.3, 1.0),  # Fioletowe światło
        intensity=0.5
    )

    lights = [light1, light2, light3, light4, light5, light6]

    # Aktualny materiał
    current_material_index = 0
    material_names = list(MATERIALS.keys())
    current_material = MATERIALS[material_names[current_material_index]]

    # Wyświetlanie instrukcji
    print("\n=== Interaktywna aplikacja modelu odbicia Phonga ===")
    print("Sterowanie:")
    print("  W/S/A/D - poruszanie kamerą przód/tył/lewo/prawo")
    print("  Q/E - ruch kamery góra/dół")
    print("  Strzałki - obracanie kamery")
    print("  Spacja - zmiana materiału")
    print("  1-6 - włączanie/wyłączanie źródeł światła")
    print("  ESC - wyjście z aplikacji")
    print(f"Aktualny materiał: {current_material.name}")
    print("\nOpis świateł:")
    print("  1 - Ciepłe, żółtawe światło (z przodu po prawej)")
    print("  2 - Chłodne, niebieskawe światło (z przodu po lewej)")
    print("  3 - Białe światło (z góry)")
    print("  4 - Zielone światło (z dołu)")
    print("  5 - Czerwone światło (z tyłu)")
    print("  6 - Fioletowe światło (po prawej i z tyłu)")

    # Flagi włączenia świateł
    lights_enabled = [True, True, True, True, True, True]

    # Główna pętla gry
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_SPACE:
                    # Zmiana materiału
                    current_material_index = (current_material_index + 1) % len(material_names)
                    current_material = MATERIALS[material_names[current_material_index]]
                    print(f"Aktualny materiał: {current_material.name}")
                elif event.key == K_1:
                    # Włączanie/wyłączanie pierwszego światła
                    lights_enabled[0] = not lights_enabled[0]
                    print(f"Światło 1 (ciepłe, żółtawe): {'włączone' if lights_enabled[0] else 'wyłączone'}")
                elif event.key == K_2:
                    # Włączanie/wyłączanie drugiego światła
                    lights_enabled[1] = not lights_enabled[1]
                    print(f"Światło 2 (chłodne, niebieskawe): {'włączone' if lights_enabled[1] else 'wyłączone'}")
                elif event.key == K_3:
                    # Włączanie/wyłączanie trzeciego światła
                    lights_enabled[2] = not lights_enabled[2]
                    print(f"Światło 3 (białe z góry): {'włączone' if lights_enabled[2] else 'wyłączone'}")
                elif event.key == K_4:
                    # Włączanie/wyłączanie czwartego światła
                    lights_enabled[3] = not lights_enabled[3]
                    print(f"Światło 4 (zielone z dołu): {'włączone' if lights_enabled[3] else 'wyłączone'}")
                elif event.key == K_5:
                    # Włączanie/wyłączanie piątego światła
                    lights_enabled[4] = not lights_enabled[4]
                    print(f"Światło 5 (czerwone z tyłu): {'włączone' if lights_enabled[4] else 'wyłączone'}")
                elif event.key == K_6:
                    # Włączanie/wyłączanie szóstego światła
                    lights_enabled[5] = not lights_enabled[5]
                    print(f"Światło 6 (fioletowe): {'włączone' if lights_enabled[5] else 'wyłączone'}")

        # Obsługa klawiatury do poruszania kamerą
        keys = pygame.key.get_pressed()

        # Ruch przód/tył/lewo/prawo
        if keys[K_w]:
            camera_pos.z -= camera_speed
        if keys[K_s]:
            camera_pos.z += camera_speed
        if keys[K_a]:
            camera_pos.x -= camera_speed
        if keys[K_d]:
            camera_pos.x += camera_speed

        # Ruch góra/dół
        if keys[K_q]:
            camera_pos.y += camera_speed
        if keys[K_e]:
            camera_pos.y -= camera_speed

        # Obrót kamery
        if keys[K_UP]:
            camera_rotation[0] += rotation_speed
        if keys[K_DOWN]:
            camera_rotation[0] -= rotation_speed
        if keys[K_LEFT]:
            camera_rotation[1] += rotation_speed
        if keys[K_RIGHT]:
            camera_rotation[1] -= rotation_speed

        # Czyszczenie buforów
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Ustawienie widoku kamery
        glLoadIdentity()
        glRotatef(camera_rotation[0], 1, 0, 0)
        glRotatef(camera_rotation[1], 0, 1, 0)
        glTranslatef(-camera_pos.x, -camera_pos.y, -camera_pos.z)

        # Tworzenie listy aktywnych świateł
        active_lights = []
        for i, light in enumerate(lights):
            if lights_enabled[i]:
                active_lights.append(light)

        # Rysowanie kuli z naszym modelem odbicia Phonga
        glBegin(GL_TRIANGLES)
        for face in indices:
            for idx in face:
                vertex = vertices[idx]
                normal = normals[idx]

                # Obliczenie kierunku patrzenia (od punktu do kamery)
                view_dir = Point3D(
                    camera_pos.x - vertex.x,
                    camera_pos.y - vertex.y,
                    camera_pos.z - vertex.z
                ).normalize()

                # Obliczenie koloru za pomocą modelu Phonga
                color = phong_reflection(vertex, normal, view_dir, current_material, active_lights)

                # Ustawienie koloru wierzchołka
                glColor3f(color.r, color.g, color.b)

                # Ustawienie normalnej i wierzchołka
                glNormal3f(normal.x, normal.y, normal.z)
                glVertex3f(vertex.x, vertex.y, vertex.z)
        glEnd()

        # Rysowanie źródeł światła (małe kulki)
        for light in active_lights:
            glPushMatrix()
            glTranslatef(light.position.x, light.position.y, light.position.z)
            glColor3f(light.color.r, light.color.g, light.color.b)
            # Mała kulka reprezentująca źródło światła
            quadric = gluNewQuadric()
            gluSphere(quadric, 0.1, 10, 10)
            gluDeleteQuadric(quadric)
            glPopMatrix()

        # Aktualizacja ekranu
        pygame.display.flip()
        clock.tick(60)  # Limit 60 FPS

    pygame.quit()

if __name__ == "__main__":
    main()