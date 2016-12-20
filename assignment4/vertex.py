from enum import Enum

import math

RIGHT, LEFT, EQUAL = (1, -1, 0)
EPS = 1e-6


def get_point_orientation_relative_to_line(point, line):
    start = line[0]
    end = line[1]
    if point == start or point == end:
        return EQUAL

    result = start.x * end.y + end.x * point.y + point.x * start.y - end.x * start.y - start.x * point.y - point.x * end.y
    sign = -1 if result < 0 else 1
    result = math.fabs(result)

    if result > EPS:
        if sign == 1:
            return RIGHT

        else:
            return LEFT
    return EQUAL


class VertexType(Enum):
    START = 'start'
    END = 'end'
    SPLIT = 'split'
    MERGE = 'merge'
    REGULAR = 'regular'

    @staticmethod
    def get_vertex_type(before, current, after):
        direction = get_point_orientation_relative_to_line(after, [current, before])
        if current > before and current > after:
            return VertexType.END if direction == LEFT else VertexType.MERGE
        if current < before and current < after:
            return VertexType.START if direction == LEFT else VertexType.SPLIT
        return VertexType.REGULAR



class Vertex:
    def __init__(self, x, y):
        self.y = float(y)
        self.x = float(x)

    def __lt__(self, other):
        return False if math.fabs(other.y - self.y) < EPS or self.y < other.y else True

    def __eq__(self, other):
        return True if math.fabs(other.y - self.y) < EPS else False

    def __hash__(self):
        return (53 + hash(round(self.x, 3))) * 53 + hash(round(self.y, 3))

    def __repr__(self):
        return '(' + str(self.x) + ", " + str(self.y) + ")"

