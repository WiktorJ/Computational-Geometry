# Graham Scan - Tom Switzer <thomas.switzer@gmail.com>
from functools import cmp_to_key
import time
import math
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


def get_cosine_angle(min_point, point):
    rel_x = point[0] - min_point[0]
    rel_y = point[1] - min_point[1]
    return rel_x / math.sqrt(rel_x ** 2 + rel_y ** 2)


def convex_hull(points, data_set_name):
    write_tuple_to_file(output_dir + data_set_name + "/points.csv", points)
    start_time = time.time()
    min_point = min(points, key=lambda x: (x[1], x[0]))
    comp_func = order(min_point)
    points = [x for x in points if x[0] != min_point[0] or x[1] != min_point[1]]
    points = sorted(points, key=cmp_to_key(comp_func))
    points.insert(0, min_point)

    print("--- %s seconds ---" % (time.time() - start_time))
    result = []
    for i, p in enumerate(points):
        _keep_left(result, p, i, output_dir + data_set_name)


output_dir = "graham/"

# convex_hull([(float(x), float(y)) for x, y in read_file_to_tuples('data_set_1.csv')], "graham1")
# convex_hull([(float(x), float(y)) for x, y in read_file_to_tuples('data_set_2.csv')], "graham2")
# convex_hull([(float(x), float(y)) for x, y in read_file_to_tuples('data_set_3.csv')], "graham3")
convex_hull([(float(x), float(y)) for x, y in read_file_to_tuples('data_set_4.csv')], "graham4")
