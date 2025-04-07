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


def classify_polygon(polygon, plane_normal, plane_point):
    """
    Classifies a polygon relative to a plane and splits it if necessary.
    Returns: (classification, front_polygon, back_polygon)
    """
    EPSILON = 1e-7
    front_verts = []
    back_verts = []
    on_plane = []

    # Classify each vertex
    for vert in polygon:
        vec = vector_sub(vert, plane_point)
        dist = dot(vec, plane_normal)
        if dist > EPSILON:
            front_verts.append(vert)
        elif dist < -EPSILON:
            back_verts.append(vert)
        else:
            on_plane.append(vert)

    # All vertices on the plane or degenerate
    if not front_verts and not back_verts:
        return 'on', polygon, None

    # Entirely in front
    if not back_verts:
        return 'front', polygon, None

    # Entirely in back
    if not front_verts:
        return 'back', None, polygon

    # Split the polygon
    front_poly = []
    back_poly = []
    for i in range(len(polygon)):
        j = (i + 1) % len(polygon)
        a = polygon[i]
        b = polygon[j]
        a_dist = dot(vector_sub(a, plane_point), plane_normal)
        b_dist = dot(vector_sub(b, plane_point), plane_normal)

        # Add current vertex
        if a_dist >= -EPSILON:
            front_poly.append(a)
        if a_dist <= EPSILON:
            back_poly.append(a)

        # Check if edge crosses the plane
        if (a_dist > EPSILON and b_dist < -EPSILON) or (a_dist < -EPSILON and b_dist > EPSILON):
            t = (-a_dist) / (b_dist - a_dist)
            intersect = (
                a[0] + t * (b[0] - a[0]),
                a[1] + t * (b[1] - a[1]),
                a[2] + t * (b[2] - a[2])
            )
            front_poly.append(intersect)
            back_poly.append(intersect)

    return 'split', front_poly, back_poly


def build_bsp(polygons):
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
            back_list.append(poly_back)
        elif ctype == 'split':
            if poly_front:
                front_list.append(poly_front)
            if poly_back:
                back_list.append(poly_back)

    root.front = build_bsp(front_list)
    root.back = build_bsp(back_list)
    return root


def is_in_front_of_plane(point, plane_normal, plane_point):
    vec = vector_sub(point, plane_point)
    d = dot(vec, plane_normal)
    return (d >= 0)
