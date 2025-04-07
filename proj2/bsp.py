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


def classify_polygon(polygon, plane_normal, plane_point, camera_pos, camera_forward):
    """
    Tells whether the entire polygon is in front, behind, or straddling
    the plane defined by (plane_normal, plane_point).
    Additionally, classify based on camera's position and direction.
    """
    EPSILON = 1e-7
    front_count = 0
    back_count = 0

    # Calculate the polygon's center to classify it relative to the camera's view
    poly_center = [sum(x) / len(polygon) for x in zip(*polygon)]  # Average of all vertices

    # Vector from camera to polygon center
    camera_to_poly = vector_sub(poly_center, camera_pos)
    # Dot product between camera's forward vector and the vector to the polygon center
    dot_product = dot(camera_to_poly, camera_forward)

    for vert in polygon:
        vec = vector_sub(vert, plane_point)
        dist = dot(vec, plane_normal)
        if dist > EPSILON:
            front_count += 1
        elif dist < -EPSILON:
            back_count += 1

    # If the polygon is in front of the camera, consider it "front" for BSP partitioning
    if dot_product > 0:
        return 'front', polygon, None
    elif dot_product < 0:
        return 'back', polygon, None
    # If it's exactly in front or behind (parallel to the camera's view), treat it as front
    return 'front', polygon, None


def build_bsp(polygons, camera_pos, camera_forward):
    """
    Recursively build a BSP tree from a list of polygons, considering the camera's position and orientation.
    """
    if not polygons:
        return None

    root_poly = polygons[0]
    plane_normal, plane_point = compute_plane_normal_and_point(root_poly)
    root = BSPNode(root_poly, plane_normal, plane_point)

    front_list = []
    back_list = []

    for poly in polygons[1:]:
        ctype, poly_front, poly_back = classify_polygon(poly, plane_normal, plane_point, camera_pos, camera_forward)
        if ctype == 'front':
            front_list.append(poly_front)
        elif ctype == 'back':
            back_list.append(poly_front)

    root.front = build_bsp(front_list, camera_pos, camera_forward)
    root.back = build_bsp(back_list, camera_pos, camera_forward)

    return root


def is_in_front_of_plane(point, plane_normal, plane_point):
    vec = vector_sub(point, plane_point)
    d = dot(vec, plane_normal)
    return (d >= 0)
