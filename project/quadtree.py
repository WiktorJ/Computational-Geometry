from pprint import pformat

from matplotlib import pyplot as plt

from generator_utils import generate_in_range
from project.draw_utils import prepare_subplot

NODE_CAPACITY = 1

c_range = ((3, 5), (8, 9))
draw_range = True

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

    def insert(self, point, draw_point, draw_division):

        if not self.rect.contains(point):
            return False

        if len(self.points) < NODE_CAPACITY:
            self.points.append(point)
            draw_point(point)
            return True

        if not self.northWest.region_exists():
            draw_division(self.rect)
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

    def range_search(self, c_range, draw):

        points = []

        if not self.rect.intersects(c_range):
            return points

        for point in self.points:
            if c_range.contains(point):
                draw(point)
                points.append(point)

        if not self.northWest.region_exists():
            return points

        points += self.northWest.range_search(c_range)
        points += self.northEast.range_search(c_range)
        points += self.southWest.range_search(c_range)
        points += self.southEast.range_search(c_range)

        return points

    def draw_tree(self):
        pass

    def __repr__(self):
        return pformat((self.points, self.northWest, self.northEast, self.southWest, self.southEast))


class NoExistingRegion(Node):
    def __init__(self):
        super().__init__(AABB((0, 0), (0, 0)))

    def region_exists(self):
        return False

    def subdivide(self):
        raise Exception("Unsupported operation, subdivide on NoExistingRegion")

    def insert(self, point, draw_point, draw_division):
        return False

    def range_search(self, c_range, draw):
        return []

    def __repr__(self):
        return "_"


def quad_tree(points, rect, draw_point, draw_division):
    tree = Node(rect)
    for point in points:
        tree.insert(point, draw_point, draw_division)
    return tree

def draw_subdivision_on_subplot(ax):
    def draw_subdivision(rect):
        new_rect = plt.Rectangle((rect.center[0] - rect.half_size[0], rect.center[1] - rect.half_size[1]), rect.half_size[0],
                             rect.half_size[1], ec='k', fc='none')
        ax.add_patch(new_rect)
        new_rect = plt.Rectangle((rect.center[0], rect.center[1] - rect.half_size[1]), rect.half_size[0],
                             rect.half_size[1], ec='k', fc='none')
        ax.add_patch(new_rect)
        new_rect = plt.Rectangle((rect.center[0] - rect.half_size[0], rect.center[1]), rect.half_size[0],
                             rect.half_size[1], ec='k', fc='none')
        ax.add_patch(new_rect)
        new_rect = plt.Rectangle((rect.center[0], rect.center[1]), rect.half_size[0],
                             rect.half_size[1], ec='k', fc='none')
        ax.add_patch(new_rect)
    return draw_subdivision


def main():
    # point_list = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2)]
    point_list = generate_in_range(0, 10, 15)
    fig = plt.figure()
    fig.subplots_adjust(wspace=0.1, hspace=0.15,
                        left=0.1, right=0.9,
                        bottom=0.05, top=0.9)

    ax = prepare_subplot(fig, point_list, 1, 1, 1)
    aabb = AABB((0, 0), (10, 10))
    if not draw_range:
        tree = quad_tree(point_list, aabb, lambda *args: None, lambda *args: None)
        tree.range_search(AABB.from_points(((3, 0), (8, 10))),
                          lambda *args: None)
    else:
        rect = plt.Rectangle(c_range[0], c_range[1][0] - c_range[0][0],
                             c_range[1][1] - c_range[0][1], ec='k', fc='none', edgecolor='red', linestyle='dashed',
                             linewidth='3')
        ax.add_patch(rect)
        tree = quad_tree(point_list, aabb, lambda point: ax.scatter([point[0]], [point[1]], s=22, color='red'), draw_subdivision_on_subplot(ax))
        tree.range_search(AABB.from_points(((3, 0), (8, 10))), lambda point: ax.scatter([point[0]], [point[1]], s=22, color='red'))
    plt.show()

if __name__ == '__main__':
    main()
