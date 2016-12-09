from enum import Enum

import math

ABOVE, BELOW, EQUAL = (1, -1, 0)
EPS = 1e-6


def get_point_orientation_relative_to_line(point, line):
    start = line.start
    end = line.end
    if point == start or point == end:
        return EQUAL

    result = start.x * end.y + end.x * point.y + point.x * start.y - end.x * start.y - start.x * point.y - point.x * end.y
    sign = -1 if result < 0 else 1
    result = math.fabs(result)

    if result > EPS:
        if sign == 1:
            return ABOVE

        else:
            return BELOW
    return EQUAL


class EventType(Enum):
    start = 'segment start'
    end = 'segment end'
    intersection = 'segments intersection'


class Point:
    def __init__(self, x, y):
        self.y = y
        self.x = x

    def to_tuple(self):
        return self.x, self.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self, *args, **kwargs):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __hash__(self):
        return (53 + hash(round(float(self.x), 3))) * 53 + hash(round(float(self.y), 3))


class StateSegment:
    def __init__(self, segment):
        self.segment = segment
        self.start = segment.start
        self.end = segment.end
        self.orientation_point = segment.start

    def to_tuple(self):
        return self.segment.to_tuple()



    def from_tuple(cls, raw_tuple):
        return cls(Segment.from_tuple(raw_tuple))

    def __lt__(self, other):
        if self.orientation_point.x >= other.orientation_point.x:
            orientation = get_point_orientation_relative_to_line(self.orientation_point, other.segment)
        else:
            orientation = -get_point_orientation_relative_to_line(other.orientation_point, self.segment)

        return True if orientation == ABOVE or \
                       (orientation == EQUAL and
                        get_point_orientation_relative_to_line(self.end, other.segment) == ABOVE) else False

    def __eq__(self, other):
        return True if get_point_orientation_relative_to_line(self.orientation_point, other.segment) == EQUAL else False


class Segment:
    def __init__(self, start, end):
        self.end = end
        self.start = start

    def to_tuple(self):
        return self.start.to_tuple() + self.end.to_tuple()

    @classmethod
    def from_tuple(cls, raw_tuple):
        start = raw_tuple[0]
        end = raw_tuple[1]
        if end[0] < start[0]:
            start, end = end, start
        return cls(Point(start[0], start[1]), Point(end[0], end[1]))

    def __eq__(self, other):
        return self.end == other.end and self.start == other.start

    def __repr__(self, *args, **kwargs):
        return "[" + str(self.start) + ", " + str(self.end) + "]"


class Event:
    # todo: Update lt, gt and eq functions to support case when there are two events with the same x
    def __init__(self, point, segments, event_type):
        self.segments = segments
        self.point = point
        self.type = event_type

    def __lt__(self, other):
        return True if self.point.x < other.point.x or (
            self.point.x == other.point.x and self.point.y < other.point.y) else False

    def __gt__(self, other):
        return True if self.point.x > other.point.x or (
            self.point.x == other.point.x and self.point.y > other.point.y) else False

    def __eq__(self, other):
        return True if math.isclose(self.point.x, other.point.x, rel_tol=1e-4) and \
                       math.isclose(self.point.y, other.point.y, rel_tol=1e-4) else False

    def __hash__(self, *args, **kwargs):
        return hash(self.point)


class Intersection(Event):
    def __init__(self, point, segment1, segment2):
        super().__init__(point, [segment1, segment2], EventType.intersection)
        self.segment1 = segment1
        self.segment2 = segment2

    def to_tuple(self):
        return self.segment1.to_tuple() + self.segment2.to_tuple()

    def point_to_tuple(self):
        return self.point.to_tuple()

    def __repr__(self):
        return "Intersection in point " + str(self.point) + " between segment: " + str(self.segment1) + " and: " + str(
            self.segment2)

    def __eq__(self, other):
        return self.segment1 == other.segment1 and self.segment2 == other.segment2

    def __hash__(self, *args, **kwargs):
        return (((13 + hash(self.segment1.start)) * (11 + hash(self.segment1.end))) * (7 + hash(self.segment2.start)) *
                (5 + hash(self.segment2.end)))
