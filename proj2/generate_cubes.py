import json


def save_cube_data(filename):
    polygons = generate_cube_grid()

    serializable = []
    for polygon in polygons:
        serializable.append([
            [float(coord) for coord in point] for point in polygon
        ])

    with open(filename, 'w') as f:
        json.dump(serializable, f)


def generate_cube_grid():
    size = 3
    polygons = []
    spacing = 1
    cube_size = 1.2

    for x in range(size):
        for y in range(size):
            for z in range(size):
                base_x = x * (cube_size + spacing)
                base_y = y * (cube_size + spacing)
                base_z = z * (cube_size + spacing)

                v0 = (base_x, base_y, base_z)
                v1 = (base_x + cube_size, base_y, base_z)
                v2 = (base_x + cube_size, base_y + cube_size, base_z)
                v3 = (base_x, base_y + cube_size, base_z)
                v4 = (base_x, base_y, base_z + cube_size)
                v5 = (base_x + cube_size, base_y, base_z + cube_size)
                v6 = (base_x + cube_size, base_y + cube_size, base_z + cube_size)
                v7 = (base_x, base_y + cube_size, base_z + cube_size)

                polygons.append([v0, v3, v2, v1])
                polygons.append([v4, v5, v6, v7])
                polygons.append([v0, v1, v5, v4])
                polygons.append([v1, v2, v6, v5])
                polygons.append([v2, v3, v7, v6])
                polygons.append([v3, v0, v4, v7])

    return polygons


def generate_edges_from_polygons(polygons):
    edges = set()

    for poly in polygons:
        for i in range(len(poly)):
            v1 = poly[i]
            v2 = poly[(i + 1) % len(poly)]

            if v1 < v2:
                edge = (v1, v2)
            else:
                edge = (v2, v1)

            edges.add(edge)

    return list(edges)


def save_both_formats(filename_polygons, filename_edges):
    polygons = generate_cube_grid()
    edges = generate_edges_from_polygons(polygons)

    serializable_polygons = []
    for polygon in polygons:
        serializable_polygons.append([
            [float(coord) for coord in point] for point in polygon
        ])

    with open(filename_polygons, 'w') as f:
        json.dump(serializable_polygons, f)

    serializable_edges = []
    for edge in edges:
        serializable_edges.append([
            [float(coord) for coord in edge[0]],
            [float(coord) for coord in edge[1]]
        ])

    with open(filename_edges, 'w') as f:
        json.dump(serializable_edges, f)


if __name__ == "__main__":
    save_cube_data("cube_polygons.json")

    edges_polygons = generate_edges_from_polygons(generate_cube_grid())

    serializable_edges = []
    for edge in edges_polygons:
        serializable_edges.append([
            [float(coord) for coord in edge[0]],
            [float(coord) for coord in edge[1]]
        ])

    with open("cube_data.json", 'w') as f:
        json.dump(serializable_edges, f)
