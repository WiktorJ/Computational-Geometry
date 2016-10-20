# Graham Scan - Tom Switzer <thomas.switzer@gmail.com>

from functools import reduce
import csv

TURN_LEFT, TURN_RIGHT, TURN_NONE = (1, -1, 0)


def turn(p, q, r):
    det = (q[0] - p[0]) * (r[1] - p[1]) - (r[0] - p[0]) * (q[1] - p[1])
    if det < 0:
        return -1
    if det > 0:
        return 1
    return 0


def _keep_left(hull, r):
    while len(hull) > 1 and turn(hull[-2], hull[-1], r) != TURN_LEFT:
        hull.pop()
    if not len(hull) or hull[-1] != r:
        hull.append(r)
    return hull


def convex_hull(points):
    """Returns points on convex hull of an array of points in CCW order."""
    points = sorted(points)
    l = reduce(_keep_left, points, [])
    u = reduce(_keep_left, reversed(points), [])
    return l.extend(u[i] for i in range(1, len(u) - 1)) or l

def read_file_to_tuples(path):
    print('opening file', path)
    with open(path) as the_file:
        return [tuple(line) for line in csv.reader(the_file, delimiter=" ")]


points = [(float(x), float(y)) for x, y in read_file_to_tuples('data_set_1.csv')]
print(convex_hull(points))