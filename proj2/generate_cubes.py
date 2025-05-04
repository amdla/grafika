import json


def save_cube_data(filename):
    cube_data = generate_cube_grid()

    serializable = []
    for face in cube_data:
        serializable_face = []
        for point in face:
            serializable_face.append([float(coord) for coord in point])
        serializable.append(serializable_face)

    with open(filename, 'w') as f:
        json.dump(serializable, f)


def generate_cube_grid():
    size = 3
    cubes = []
    spacing = 1
    cube_size = 1.2
    for x in range(size):
        for y in range(size):
            for z in range(size):
                base_x = x * (cube_size + spacing)
                base_y = y * (cube_size + spacing)
                base_z = z * (cube_size + spacing)

                faces = [
                    # Front face
                    (
                        (base_x, base_y, base_z),
                        (base_x + cube_size, base_y, base_z),
                        (base_x + cube_size, base_y + cube_size, base_z),
                        (base_x, base_y + cube_size, base_z)
                    ),
                    # Back face
                    (
                        (base_x, base_y, base_z + cube_size),
                        (base_x + cube_size, base_y, base_z + cube_size),
                        (base_x + cube_size, base_y + cube_size, base_z + cube_size),
                        (base_x, base_y + cube_size, base_z + cube_size)
                    ),
                    # Top face
                    (
                        (base_x, base_y + cube_size, base_z),
                        (base_x + cube_size, base_y + cube_size, base_z),
                        (base_x + cube_size, base_y + cube_size, base_z + cube_size),
                        (base_x, base_y + cube_size, base_z + cube_size)
                    ),
                    # Bottom face
                    (
                        (base_x, base_y, base_z),
                        (base_x + cube_size, base_y, base_z),
                        (base_x + cube_size, base_y, base_z + cube_size),
                        (base_x, base_y, base_z + cube_size)
                    ),
                    # Left face
                    (
                        (base_x, base_y, base_z),
                        (base_x, base_y, base_z + cube_size),
                        (base_x, base_y + cube_size, base_z + cube_size),
                        (base_x, base_y + cube_size, base_z)
                    ),
                    # Right face
                    (
                        (base_x + cube_size, base_y, base_z),
                        (base_x + cube_size, base_y + cube_size, base_z),
                        (base_x + cube_size, base_y + cube_size, base_z + cube_size),
                        (base_x + cube_size, base_y, base_z + cube_size)
                    )
                ]
                cubes.extend(faces)
    return cubes
