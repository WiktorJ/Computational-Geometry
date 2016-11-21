from pprint import pformat

NODE_CAPACITY = 1


class AABB:
    def __init__(self, center, half_size):
        self.half_size = half_size
        self.center = center

    @classmethod
    def from_points(cls, points):
        half_size = (points[1][0] - points[0][0]) / 2, (points[1][1] - points[0][1]) / 2
        center = (points[1][0] - points[0][0]) / 2 + points[0][0], (points[1][1] - points[0][1]) / 2 + points[0][1]
        return AABB(center, half_size)

    def contains(self, point):
        return self.center[0] + self.half_size[0] >= point[0] >= self.center[0] - self.half_size[0] and \
               self.center[1] + self.half_size[1] >= point[1] >= self.center[1] - self.half_size[1]

    def intersects(self, other):
        return self.center[0] + self.half_size[0] > other.center[0] - other.half_size[0] and \
               self.center[0] - self.half_size[0] < other.center[0] + other.half_size[0] and \
               self.center[1] + self.half_size[1] > other.center[1] - other.half_size[1] and \
               self.center[1] - self.half_size[1] < other.center[1] + other.half_size[1]


class Node:
    def __init__(self, rect):
        self.rect = rect
        self.points = []
        if self.region_exists():
            self.northWest = NoExistingRegion()
            self.northEast = NoExistingRegion()
            self.southWest = NoExistingRegion()
            self.southEast = NoExistingRegion()

    def insert(self, point):

        if not self.rect.contains(point):
            return False

        if len(self.points) < NODE_CAPACITY:
            self.points.append(point)
            return True

        if not self.northWest.region_exists():
            self.subdivide()

        if self.northWest.insert(point): return True
        if self.northEast.insert(point): return True
        if self.southWest.insert(point): return True
        if self.southEast.insert(point): return True
        return False

    def region_exists(self):
        return True

    def subdivide(self):
        half_size = self.rect.half_size[0] / 2, self.rect.half_size[1] / 2
        center = self.rect.center[0] - half_size[0], self.rect.center[1] - half_size[1]
        self.southWest = Node(AABB(center, half_size))

        center = self.rect.center[0] - half_size[0], self.rect.center[1] + half_size[1]
        self.northWest = Node(AABB(center, half_size))

        center = self.rect.center[0] + half_size[0], self.rect.center[1] - half_size[1]
        self.southEast = Node(AABB(center, half_size))

        center = self.rect.center[0] + half_size[0], self.rect.center[1] + half_size[1]
        self.northEast = Node(AABB(center, half_size))

    def range_search(self, c_range):

        points = []

        if not self.rect.intersects(c_range):
            return points

        for point in self.points:
            if c_range.contains(point):
                points.append(point)

        if not self.northWest.region_exists():
            return points

        points += self.northWest.range_search(c_range)
        points += self.northEast.range_search(c_range)
        points += self.southWest.range_search(c_range)
        points += self.southEast.range_search(c_range)

        return points

    def __repr__(self):
        return pformat((self.points, self.northWest, self.northEast, self.southWest, self.southEast))


class NoExistingRegion(Node):
    def __init__(self):
        super().__init__(AABB((0, 0), (0, 0)))

    def region_exists(self):
        return False

    def subdivide(self):
        raise Exception("Unsupported operation, subdivide on NoExistingRegion")

    def insert(self, point):
        return False

    def range_search(self, c_range):
        return []

    def __repr__(self):
        return "_"


def quad_tree(points, rect):
    tree = Node(rect)
    for point in points:
        tree.insert(point)
    return tree


def main():
    point_list = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2)]
    tree = quad_tree(point_list, AABB((0, 0), (10, 10)))
    print(tree)
    print(tree.range_search(AABB.from_points(((3, 0), (8, 10)))))


if __name__ == '__main__':
    main()
