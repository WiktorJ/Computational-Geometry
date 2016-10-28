from assignment3.sweep_elements import Segment, Point
from generator_utils import generate_in_range


def get_random_segments(lower_bound, upper_bound, amount):
    segments = []
    for _ in range(0, amount):
        points = generate_in_range(lower_bound, upper_bound, 2)
        segments.append(Segment(Point(points[0][0], points[0][1]),
                                Point(points[1][0], points[1][1])))

    return segments

