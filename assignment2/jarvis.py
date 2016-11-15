# Jarvis March O(nh) - Tom Switzer <thomas.switzer@gmail.com>
import time

from assignment2.commons import filter_inline_points
from custom_file_utils import read_file_to_tuples, write_tuple_to_file

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


def convex_hull(points, data_set_name):
    start_time = time.time()
    min_point = min(points, key=lambda x: (x[1], x[0]))
    # points.remove(min_point)
    # points = sorted(points)
    # points = filter_inline_points(points, min_point)
    # points = sorted(points, key=lambda x: (x[1], x[0]))
    # points = filter_inline_points(points, min_point)

    # write_tuple_to_file(output_dir + data_set_name + "/points.csv", points)
    alg_start_time = time.time()
    hull = [min_point]
    for i, p in enumerate(hull):
        q = _next_hull_pt(points, p)
        if q != hull[0]:
            hull.append(q)
            # write_tuple_to_file(output_dir + data_set_name + "/" + str(i) + ".csv", hull)

    print("--- %s ms with sorting ---" % ((time.time() - start_time) * 1000))
    print("--- %s ms without sorting ---" % ((time.time() - alg_start_time) * 1000))
    return hull


output_dir = "jarvis/"

convex_hull([(float(x), float(y)) for x, y in read_file_to_tuples('data_set_1.csv')], "jarvis1")
convex_hull([(float(x), float(y)) for x, y in read_file_to_tuples('data_set_2.csv')], "jarvis2")
convex_hull([(float(x), float(y)) for x, y in read_file_to_tuples('data_set_3.csv')], "jarvis3")
convex_hull([(float(x), float(y)) for x, y in read_file_to_tuples('data_set_4.csv')], "jarvis4")
