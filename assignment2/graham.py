from functools import cmp_to_key
import time
import math

from assignment2.commons import filter_inline_points
from custom_file_utils import read_file_to_tuples, write_tuple_to_file

TURN_LEFT, TURN_RIGHT, TURN_NONE = (1, -1, 0)


def turn(p, q, r):
    det = (q[0] - p[0]) * (r[1] - p[1]) - (r[0] - p[0]) * (q[1] - p[1])
    if det < 0:
        return -1
    if det > 0:
        return 1
    return 0


def order(min_point):
    def comparator(p, q):
        t = turn(min_point, p, q)
        if t == TURN_LEFT:
            return -1
        elif t == TURN_RIGHT:
            return 1
        else:
            p_dist = sqrt_dist(min_point, p)
            q_dist = sqrt_dist(min_point, q)
            if p_dist > q_dist:
                return 1
            else:
                return -1

    return comparator


def sqrt_dist(p, q):
    rel_x = p[0] - q[0]
    rel_y = p[1] - q[1]
    return rel_x ** 2 + rel_y ** 2


def _keep_left(hull, r, i, output_dir):
    while len(hull) > 1 and turn(hull[-2], hull[-1], r) != TURN_LEFT:
        hull.pop()
    if not len(hull) or hull[-1] != r:
        hull.append(r)
    write_tuple_to_file(output_dir + "/" + str(i) + ".csv", hull)
    return hull


def convex_hull(points, data_set_name):
    start_time = time.time()
    min_point = min(points, key=lambda x: (x[1], x[0]))
    points = [x for x in points if x[0] != min_point[0] or x[1] != min_point[1]]
    points = sorted(points, key=cmp_to_key(order(min_point)))
    # print("min: ", min_point)
    # points.insert(0, min_point)
    filtered_points = [min_point]

    while len(points) > 1:
        p = points.pop(0)
        # print(p, turn(min_point, p, points[0]))
        if turn(min_point, p, points[0]) != 0:
            filtered_points.append(p)
    filtered_points.append(points[0])
    points = filtered_points
    points = filter_inline_points(points, min_point)

    write_tuple_to_file(output_dir + data_set_name + "/points.csv", points)
    alg_start_time = time.time()
    result = []
    for i, p in enumerate(points):
        _keep_left(result, p, i, output_dir + data_set_name)
    print("--- %s ms ---" % ((time.time() - start_time) * 1000))
    print("--- %s ms without sorting ---" % ((time.time() - alg_start_time) * 1000))

output_dir = "graham/"

convex_hull([(float(x), float(y)) for x, y in read_file_to_tuples('data_set_1.csv')], "graham1")
convex_hull([(float(x), float(y)) for x, y in read_file_to_tuples('data_set_2.csv')], "graham2")
convex_hull([(float(x), float(y)) for x, y in read_file_to_tuples('data_set_3.csv')], "graham3")
convex_hull([(float(x), float(y)) for x, y in read_file_to_tuples('data_set_4.csv')], "graham4")
