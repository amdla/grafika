import json


def save_cube_data(filename):
    cube_data = generate_cube_grid()

    serializable = []
    for edge in cube_data:
        serializable.append([
            [float(coord) for coord in edge[0]],
            [float(coord) for coord in edge[1]]
        ])

    with open(filename, 'w') as f:
        json.dump(serializable, f)


def generate_cube_grid():
    size = 8
    cubes = []
    spacing = 1
    cube_size = 1.2
    for x in range(size):
        for y in range(size):
            for z in range(size):
                base_x = x * (cube_size + spacing)
                base_y = y * (cube_size + spacing)
                base_z = z * (cube_size + spacing)

                edges = [
                    ((base_x, base_y, base_z), (base_x + cube_size, base_y, base_z)),
                    ((base_x + cube_size, base_y, base_z), (base_x + cube_size, base_y + cube_size, base_z)),
                    ((base_x + cube_size, base_y + cube_size, base_z), (base_x, base_y + cube_size, base_z)),
                    ((base_x, base_y + cube_size, base_z), (base_x, base_y, base_z)),
                    ((base_x, base_y, base_z + cube_size), (base_x + cube_size, base_y, base_z + cube_size)),
                    ((base_x + cube_size, base_y, base_z + cube_size),
                     (base_x + cube_size, base_y + cube_size, base_z + cube_size)),
                    ((base_x + cube_size, base_y + cube_size, base_z + cube_size),
                     (base_x, base_y + cube_size, base_z + cube_size)),
                    ((base_x, base_y + cube_size, base_z + cube_size), (base_x, base_y, base_z + cube_size)),
                    ((base_x, base_y, base_z), (base_x, base_y, base_z + cube_size)),
                    ((base_x + cube_size, base_y, base_z), (base_x + cube_size, base_y, base_z + cube_size)),
                    ((base_x + cube_size, base_y + cube_size, base_z),
                     (base_x + cube_size, base_y + cube_size, base_z + cube_size)),
                    ((base_x, base_y + cube_size, base_z), (base_x, base_y + cube_size, base_z + cube_size)),
                ]
                cubes.extend(edges)
    return cubes
