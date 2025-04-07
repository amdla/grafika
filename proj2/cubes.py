# cubes.py

# Define the vertices of a unit cube centered at the origin (0, 0, 0)
vertices = [
    (-1, -1, -1),  # 0
    (1, -1, -1),  # 1
    (1, 1, -1),  # 2
    (-1, 1, -1),  # 3
    (-1, -1, 1),  # 4
    (1, -1, 1),  # 5
    (1, 1, 1),  # 6
    (-1, 1, 1),  # 7
]

# Define the faces of the cube using the vertices
# Each face is a polygon defined by 3 or 4 vertices (quads or triangles)
cube_faces = [
    [vertices[0], vertices[1], vertices[2], vertices[3]],  # Front face
    [vertices[4], vertices[5], vertices[6], vertices[7]],  # Back face
    [vertices[0], vertices[1], vertices[5], vertices[4]],  # Bottom face
    [vertices[2], vertices[3], vertices[7], vertices[6]],  # Top face
    [vertices[1], vertices[2], vertices[6], vertices[5]],  # Right face
    [vertices[0], vertices[3], vertices[7], vertices[4]],  # Left face
]

# The cube data will be a list of these faces (polygons)
cube_data = cube_faces
