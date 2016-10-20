# Jarvis March O(nh) - Tom Switzer <thomas.switzer@gmail.com>
import csv

TURN_LEFT, TURN_RIGHT, TURN_NONE = (1, -1, 0)


def turn(p, q, r):
    """Returns -1, 0, 1 if p,q,r forms a right, straight, or left turn."""
    det = (q[0] - p[0]) * (r[1] - p[1]) - (r[0] - p[0]) * (q[1] - p[1])
    if det < 0:
        return -1
    if det > 0:
        return 1
    return 0


def _dist(p, q):
    """Returns the squared Euclidean distance between p and q."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    return dx ** 2 + dy ** 2


def _next_hull_pt(points, p):
    """Returns the next point on the convex hull in CCW from p."""
    q = p
    for r in points:
        t = turn(p, q, r)
        if t == TURN_RIGHT or t == TURN_NONE and _dist(p, r) > _dist(p, q):
            q = r
    return q


def convex_hull(points):
    """Returns the points on the convex hull of points in CCW order."""
    hull = [min(points)]
    for p in hull:
        q = _next_hull_pt(points, p)
        if q != hull[0]:
            hull.append(q)
    return hull


def read_file_to_tuples(path):
    print('opening file', path)
    with open(path) as the_file:
        return [tuple(line) for line in csv.reader(the_file, delimiter=" ")]


points = [(float(x), float(y)) for x, y in read_file_to_tuples('data_set_1.csv')]
print(convex_hull(points))
