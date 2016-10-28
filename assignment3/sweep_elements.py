from enum import Enum

import math

ABOVE, BELOW, EQUAL = (1, -1, 0)
EPS = 1e-6


def get_point_orientation_relative_to_line(point, line):
    start = line.start
    end = line.end
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


class StateSegment:
    def __init__(self, segment):
        self.segment = segment

    def to_tuple(self):
        return self.segment.to_tuple()

    @classmethod
    def from_tuple(cls, raw_tuple):
        return cls(Segment.from_tuple(raw_tuple))

    def __lt__(self, other):
        return True if get_point_orientation_relative_to_line(self.segment.start, other.segment) == ABOVE else False

    def __gt__(self, other):
        return True if get_point_orientation_relative_to_line(self.segment.start, other.segment) == BELOW else False

    def __eq__(self, other):
        return True if get_point_orientation_relative_to_line(self.segment.start, other.segment) == EQUAL else False


class Segment:
    def __init__(self, start, end):
        self.end = end
        self.start = start

    def to_tuple(self):
        return self.start.to_tuple(), self.end.to_tuple()

    @classmethod
    def from_tuple(cls, raw_tuple):
        start = raw_tuple[0]
        end = raw_tuple[1]
        if end[0] < start[0]:
            start, end = end, start
        return cls(Point(start[0], start[1]), Point(end[0], end[1]))


class Event:
    def __init__(self, point, segments, event_type):
        self.segments = segments
        self.point = point
        self.type = event_type
