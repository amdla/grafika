import math


###############################################################################
#                            BSP-Tree Data Structures
###############################################################################

class BSPNode:
    """
    Each BSP node holds:
      - polygon: the polygon (face) that 'partitions' space at this node
      - plane_normal: normal of the polygon's plane
      - plane_point: any point on that plane (to help with front/back checks)
      - front: pointer to the BSP subtree for polygons that lie in front
      - back: pointer to the BSP subtree for polygons that lie behind
    """

    def __init__(self, polygon, plane_normal, plane_point):
        self.polygon = polygon
        self.plane_normal = plane_normal
        self.plane_point = plane_point
        self.front = None
        self.back = None


###############################################################################
#                        Geometry Helper Functions
###############################################################################

def vector_sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a, b):
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0]
    )


def compute_plane_normal_and_point(polygon):
    """
    Given a polygon (list of 3D vertices),
    return (normal, point_on_plane).
    We'll just use the first 3 vertices to compute a normal.
    """
    if len(polygon) < 3:
        # Degenerate polygon
        return (0, 0, 1), polygon[0]
    p0, p1, p2 = polygon[0], polygon[1], polygon[2]
    v1 = vector_sub(p1, p0)
    v2 = vector_sub(p2, p0)
    normal = cross(v1, v2)
    return normal, p0


def classify_polygon(polygon, plane_normal, plane_point):
    """
    Tells whether the entire polygon is in front, behind, or straddling
    the plane defined by (plane_normal, plane_point).
    Returns: ('front'|'back'|'split', polygon_front, polygon_back).
    For brevity, we won't implement polygon splitting and will skip 'split'.
    """
    EPSILON = 1e-7
    front_count = 0
    back_count = 0

    for vert in polygon:
        vec = vector_sub(vert, plane_point)
        dist = dot(vec, plane_normal)
        if dist > EPSILON:
            front_count += 1
        elif dist < -EPSILON:
            back_count += 1

        if front_count and back_count:
            return 'split', None, None

    if front_count > 0 and back_count == 0:
        return 'front', polygon, None
    if back_count > 0 and front_count == 0:
        return 'back', polygon, None
    # If it's exactly on the plane or borderline, treat as front
    return 'front', polygon, None


def build_bsp(polygons):
    """
    Recursively build a BSP tree from a list of polygons.
    (Naive approach picking the first polygon as the partition plane.)
    """
    if not polygons:
        return None

    root_poly = polygons[0]
    plane_normal, plane_point = compute_plane_normal_and_point(root_poly)
    root = BSPNode(root_poly, plane_normal, plane_point)

    front_list = []
    back_list = []

    for poly in polygons[1:]:
        ctype, poly_front, poly_back = classify_polygon(poly, plane_normal, plane_point)
        if ctype == 'front':
            front_list.append(poly_front)
        elif ctype == 'back':
            back_list.append(poly_front)
        elif ctype == 'split':
            # We skip real splitting here, so just treat as front.
            front_list.append(poly)

    root.front = build_bsp(front_list)
    root.back = build_bsp(back_list)
    return root


def is_in_front_of_plane(point, plane_normal, plane_point):
    vec = vector_sub(point, plane_point)
    d = dot(vec, plane_normal)
    return (d >= 0)


###############################################################################
#                 A Simple “Cube Faces” Setup (6 Polygons)
###############################################################################
cube_faces = [
    # front face (z=+1)
    [(+1, +1, +1), (-1, +1, +1), (-1, -1, +1), (+1, -1, +1)],
    # back face (z=-1)
    [(+1, +1, -1), (+1, -1, -1), (-1, -1, -1), (-1, +1, -1)],
    # left face (x=-1)
    [(-1, +1, +1), (-1, +1, -1), (-1, -1, -1), (-1, -1, +1)],
    # right face (x=+1)
    [(+1, +1, +1), (+1, -1, +1), (+1, -1, -1), (+1, +1, -1)],
    # top face (y=+1)
    [(+1, +1, +1), (+1, +1, -1), (-1, +1, -1), (-1, +1, +1)],
    # bottom face (y=-1)
    [(+1, -1, +1), (-1, -1, +1), (-1, -1, -1), (+1, -1, -1)],
]


###############################################################################
#                       BSP Rendering Support
###############################################################################
def render_bsp(root, camera, canvas, project_point):
    """
    Traverse the BSP tree in back-to-front order from camera's point of view,
    then draw each polygon.
    """
    if root is None:
        return

    if is_in_front_of_plane(camera.pos, root.plane_normal, root.plane_point):
        # Camera is in front -> draw back side, then this polygon, then front side
        render_bsp(root.back, camera, canvas, project_point)
        draw_polygon(root.polygon, camera, canvas, project_point)
        render_bsp(root.front, camera, canvas, project_point)
    else:
        # Camera is behind -> draw front side, then this polygon, then back side
        render_bsp(root.front, camera, canvas, project_point)
        draw_polygon(root.polygon, camera, canvas, project_point)
        render_bsp(root.back, camera, canvas, project_point)


def draw_polygon(polygon, camera, canvas, project_point):
    """
    Projects the polygon to 2D and fills it, effectively hiding anything behind it.
    """
    pts_2d = []
    w = int(canvas.cget("width"))
    h = int(canvas.cget("height"))
    for v in polygon:
        p2 = project_point(v, camera, w, h)
        if not p2:
            return  # If any vertex is behind the camera, skip fill for simplicity
        pts_2d.append(p2)

    flat_coords = []
    for (sx, sy) in pts_2d:
        flat_coords.append(sx)
        flat_coords.append(sy)

    # Draw with a fill color. This overwrites anything behind it.
    canvas.create_polygon(flat_coords, fill="#cccccc", outline="black")
