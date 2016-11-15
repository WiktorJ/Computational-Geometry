from assignment3.sweep_elements import Segment, Point
from custom_file_utils import read_file_to_tuples, write_tuple_to_file
from generator_utils import generate_in_range


def get_random_segments(lower_bound, upper_bound, amount):
    segments = []
    for _ in range(0, amount):
        points = generate_in_range(lower_bound, upper_bound, 2)
        p1 = Point(points[0][0], points[0][1])
        p2 = Point(points[1][0], points[1][1])
        if p1.x < p2.x:
            segments.append(Segment(p1, p2))
        else:
            segments.append(Segment(p2, p1))

    return segments


def get_segments_from_file(path):
    return [Segment(Point(float(tup[0]), float(tup[1])), Point(float(tup[2]), float(tup[3]))) for tup in
            read_file_to_tuples(path)]


def save_segments_to_file(path, segments):
    write_tuple_to_file(path, list(map(lambda s: s.to_tuple(), segments)))
