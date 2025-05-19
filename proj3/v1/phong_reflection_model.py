import matplotlib.pyplot as plt
import numpy as np


# Funkcja tworząca siatkę punktów na powierzchni kuli
def create_sphere(radius=1.0, resolution=100):
    phi = np.linspace(0, 2 * np.pi, resolution)
    theta = np.linspace(0, np.pi, resolution)
    phi, theta = np.meshgrid(phi, theta)

    x = radius * np.sin(theta) * np.cos(phi)
    y = radius * np.sin(theta) * np.sin(phi)
    z = radius * np.cos(theta)

    return x, y, z


# Funkcja obliczająca normalne dla każdego punktu na powierzchni kuli
def compute_normals(x, y, z):
    # Dla kuli, normalne wskazują od środka (0,0,0) do punktu na powierzchni
    norm = np.sqrt(x ** 2 + y ** 2 + z ** 2)
    nx = x / norm
    ny = y / norm
    nz = z / norm

    return nx, ny, nz


# Funkcja implementująca model odbicia Phonga (BRDF)
def phong_reflection(normals, view_dir, light_dir, ka, kd, ks, shininess):
    nx, ny, nz = normals

    # Obliczanie składowej ambientowej (otoczenia)
    ambient = ka

    # Obliczanie składowej dyfuzyjnej (rozproszonej)
    # Iloczyn skalarny między wektorami normalnymi a kierunkiem światła
    dot_product = nx * light_dir[0] + ny * light_dir[1] + nz * light_dir[2]
    diffuse = kd * np.maximum(0, dot_product)

    # Obliczanie składowej zwierciadlanej (specular)
    # Obliczanie wektora odbicia światła
    reflect_x = 2 * dot_product * nx - light_dir[0]
    reflect_y = 2 * dot_product * ny - light_dir[1]
    reflect_z = 2 * dot_product * nz - light_dir[2]

    # Normalizacja wektora odbicia
    reflect_norm = np.sqrt(reflect_x ** 2 + reflect_y ** 2 + reflect_z ** 2)
    reflect_x = np.divide(reflect_x, reflect_norm, where=reflect_norm != 0)
    reflect_y = np.divide(reflect_y, reflect_norm, where=reflect_norm != 0)
    reflect_z = np.divide(reflect_z, reflect_norm, where=reflect_norm != 0)

    # Iloczyn skalarny między wektorem odbicia a kierunkiem obserwatora
    reflect_dot_view = reflect_x * view_dir[0] + reflect_y * view_dir[1] + reflect_z * view_dir[2]
    specular = ks * np.power(np.maximum(0, reflect_dot_view), shininess)

    # Końcowa intensywność światła
    intensity = ambient + diffuse + specular

    return intensity


# Funkcja do generowania obrazu kuli z modelem odbicia Phonga
def render_sphere_with_phong(material_name, ka, kd, ks, shininess, light_position, view_position, color):
    # Tworzenie kuli
    x, y, z = create_sphere(radius=1.0, resolution=100)

    # Obliczanie normalnych
    normals = compute_normals(x, y, z)

    # Normalizacja kierunku światła
    light_dir = np.array(light_position)
    light_dir = light_dir / np.linalg.norm(light_dir)

    # Normalizacja kierunku obserwatora
    view_dir = np.array(view_position)
    view_dir = view_dir / np.linalg.norm(view_dir)

    # Obliczanie intensywności odbicia za pomocą modelu Phonga
    intensity = phong_reflection(normals, view_dir, light_dir, ka, kd, ks, shininess)

    # Tworzenie koloru RGB z intensywnością
    r = np.clip(intensity * color[0], 0, 1)
    g = np.clip(intensity * color[1], 0, 1)
    b = np.clip(intensity * color[2], 0, 1)

    # Utworzenie figury
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Rysowanie kuli z odbiciem światła
    surf = ax.plot_surface(x, y, z, facecolors=np.dstack((r, g, b)), rstride=1, cstride=1)

    # Rysowanie kierunku światła
    ax.quiver(0, 0, 0, *light_dir, color='yellow', length=2, label='Kierunek światła')

    # Ustawienia osi
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f'Model odbicia Phonga: {material_name}')

    # Ustawienie równych skal osi
    max_range = np.array([x.max() - x.min(), y.max() - y.min(), z.max() - z.min()]).max() / 2.0
    mid_x = (x.max() + x.min()) * 0.5
    mid_y = (y.max() + y.min()) * 0.5
    mid_z = (z.max() + z.min()) * 0.5
    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)

    # Dodanie legendy
    ax.legend()

    # Wyświetlanie figury
    plt.tight_layout()
    plt.savefig(f"phong_reflection_{material_name.replace(' ', '_').lower()}.png")
    plt.show()

    return fig


# Główna funkcja programu
def main():
    # Parametry światła i obserwatora
    light_position = [2.0, 2.0, 3.0]  # Pozycja źródła światła
    view_position = [0.0, 0.0, 5.0]  # Pozycja obserwatora (kamery)

    # Parametry materiałów
    # Dla każdego materiału określamy:
    # ka - współczynnik ambient (otoczenia)
    # kd - współczynnik diffuse (rozproszenia)
    # ks - współczynnik zwierciadlany (specular)
    # shininess - połysk (im wyższy, tym odbicie bardziej skupione)

    # 1. Wypolerowane drewno - silna składowa rozproszona
    render_sphere_with_phong(
        material_name="Wypolerowane Drewno",
        ka=0.2,  # słabe otoczenie
        kd=0.8,  # silne rozproszenie
        ks=0.3,  # słabe odbicie kierunkowe
        shininess=10,  # niski połysk
        light_position=light_position,
        view_position=view_position,
        color=[0.6, 0.3, 0.1]  # Kolor drewna (brązowy)
    )

    # 2. Dobry plastik - silniejsza składowa kierunkowa
    render_sphere_with_phong(
        material_name="Dobry Plastik",
        ka=0.1,  # słabe otoczenie
        kd=0.4,  # średnie rozproszenie
        ks=0.7,  # silne odbicie kierunkowe
        shininess=50,  # średni połysk
        light_position=light_position,
        view_position=view_position,
        color=[0.2, 0.5, 0.7]  # Kolor plastiku (niebieskawy)
    )

    # 3. Złoto - bardzo silna składowa kierunkowa i charakterystyczny kolor
    render_sphere_with_phong(
        material_name="Złoto",
        ka=0.3,  # średnie otoczenie
        kd=0.3,  # słabe rozproszenie
        ks=1.0,  # bardzo silne odbicie kierunkowe
        shininess=100,  # wysoki połysk
        light_position=light_position,
        view_position=view_position,
        color=[1.0, 0.8, 0.0]  # Kolor złota (żółty)
    )


if __name__ == "__main__":
    main()
