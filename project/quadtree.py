from pprint import pformat

from matplotlib import pyplot as plt

from generator_utils import generate_in_range
from project.draw_utils import prepare_subplot, get_draw_point

NODE_CAPACITY = 1

c_range = ((3, 5), (8, 9))
lims = (0, 10)
draw_range = True
frame_time = 0.00001
step_draw = False
points_number = 50


class AABB:
    """
    Class that represent Square.
    """
    def __init__(self, center, half_size):
        """
        :param center: Center of square
        :param half_size: Distance from center to side of the square.
        :return:
        """
        self.half_size = half_size
        self.center = center

    @classmethod
    def from_points(cls, points):
        """
        Create AABB from left-bottom and right-up point.
        :param points:
        :return:
        """
        half_size = (points[1][0] - points[0][0]) / 2, (points[1][1] - points[0][1]) / 2
        center = (points[1][0] - points[0][0]) / 2 + points[0][0], (points[1][1] - points[0][1]) / 2 + points[0][1]
        return AABB(center, half_size)

    def contains(self, point):
        """
        :param point:
        :return: True of point lays within square.
        """
        return self.center[0] + self.half_size[0] >= point[0] >= self.center[0] - self.half_size[0] and \
               self.center[1] + self.half_size[1] >= point[1] >= self.center[1] - self.half_size[1]

    def intersects(self, other):
        """
        :param other:
        :return: True if this square intersects with other
        """
        return self.center[0] + self.half_size[0] > other.center[0] - other.half_size[0] and \
               self.center[0] - self.half_size[0] < other.center[0] + other.half_size[0] and \
               self.center[1] + self.half_size[1] > other.center[1] - other.half_size[1] and \
               self.center[1] - self.half_size[1] < other.center[1] + other.half_size[1]


class Node:
    """
    Class that represents node in tree.
    """
    def __init__(self, rect):
        self.rect = rect
        self.points = []
        if self.region_exists():
            self.northWest = NoExistingRegion()
            self.northEast = NoExistingRegion()
            self.southWest = NoExistingRegion()
            self.southEast = NoExistingRegion()

    def insert(self, point, draw_point, draw_division):
        """
        Inserts point to tree
        :param point:
        :param draw_point: Function for drawing point. Takes point.
        :param draw_division: Function for drawing new subdivision. Takes rectangle (AABB)
        :return:
        """

        if not self.rect.contains(point):
            return False

        if len(self.points) < NODE_CAPACITY:
            self.points.append(point)
            draw_point(point)
            return True

        if not self.northWest.region_exists():
            draw_division(self.rect)
            self.subdivide()

        if self.northWest.insert(point, draw_point, draw_division): return True
        if self.northEast.insert(point, draw_point, draw_division): return True
        if self.southWest.insert(point, draw_point, draw_division): return True
        if self.southEast.insert(point, draw_point, draw_division): return True
        return False

    def region_exists(self):
        """
        :return: Always true as this is regular node.
        """
        return True

    def subdivide(self):
        """
        Divides square on 4 equal parts.
        :return:
        """
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
        """
        Search for all points in given c_range
        :param c_range:
        :param draw: Function for drawing point classified within c_range.
        :return:
        """

        points = []

        if not self.rect.intersects(c_range):
            return points

        for point in self.points:
            if c_range.contains(point):
                draw(point)
                points.append(point)

        if not self.northWest.region_exists():
            return points

        points += self.northWest.range_search(c_range, draw)
        points += self.northEast.range_search(c_range, draw)
        points += self.southWest.range_search(c_range, draw)
        points += self.southEast.range_search(c_range, draw)

        return points

    def draw_tree(self):
        pass

    def __repr__(self):
        return pformat((self.points, self.northWest, self.northEast, self.southWest, self.southEast))


class NoExistingRegion(Node):
    """
    Mocked node for implementation simplicity.
    """
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


def quad_tree(points, rect, draw_point, draw_division, ax):
    """
    Creates quadtree by inserting points
    :param points:
    :param rect: Starting area
    :param draw_point:
    :param draw_division:
    :param ax:
    :return: quadtree
    """
    draw_current_point = get_draw_point(ax, plt, frame_time, step_draw, 32, 'green')
    draw_already_added_point = get_draw_point(ax, plt, frame_time, step_draw, 22, 'blue')
    tree = Node(rect)
    for point in points:
        current_point = draw_current_point(point)
        tree.insert(point, draw_point, draw_division)
        current_point.remove()
        draw_already_added_point(point)
    return tree


def draw_subdivision_on_subplot(ax):
    """
    :param ax:
    :return: Returns function that draw subdivision on given ax
    """
    def draw_subdivision(rect):
        """
        :param rect: Square to subdivide.
        :return:
        """
        new_rect = plt.Rectangle((rect.center[0] - rect.half_size[0], rect.center[1] - rect.half_size[1]),
                                 rect.half_size[0],
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

        plt.draw()
        plt.pause(frame_time)
        if step_draw:
            input("Press [enter] to continue (RECTANGLE).")

    return draw_subdivision


def main():
    # point_list = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2)]
    point_list = generate_in_range(lims[0], lims[1], points_number)
    # point_list = list(map(lambda t: (float(t[0]), float(t[1])), read_file_to_tuples('points.csv')))
    plt.ion()
    # plt.show()
    fig = plt.figure()
    fig.subplots_adjust(wspace=0.1, hspace=0.15,
                        left=0.1, right=0.9,
                        bottom=0.05, top=0.9)

    ax = prepare_subplot(fig, point_list, 1, 1, 1, lims)
    aabb = AABB.from_points(((lims[0], lims[0]), (lims[1], lims[1])))

    if not draw_range:
        tree = quad_tree(point_list, aabb, lambda *args: None, lambda *args: None, ax)
        tree.range_search(AABB.from_points(c_range),
                          lambda *args: None)
    else:
        tree = quad_tree(point_list, aabb, lambda point: ax.scatter([point[0]], [point[1]], s=9),
                         draw_subdivision_on_subplot(ax), ax)

        rect = plt.Rectangle(c_range[0], c_range[1][0] - c_range[0][0],
                             c_range[1][1] - c_range[0][1], ec='k', fc='none', edgecolor='red', linestyle='dashed',
                             linewidth='3')
        ax.add_patch(rect)
        plt.draw()
        input("Press [enter] search.")
        search = tree.range_search(AABB.from_points(c_range), get_draw_point(ax, plt, frame_time, step_draw, 22, 'red'))
        print(search)

    plt.draw()
    input("Press [enter] to finish.")
    plt.show()


if __name__ == '__main__':
    main()
