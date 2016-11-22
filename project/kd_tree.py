from collections import namedtuple
from operator import itemgetter
from pprint import pformat
import numpy as np
from matplotlib import pyplot as plt

from generator_utils import generate_in_range

k = 2

c_range = ((3, 5), (8, 9))
draw_range = True


class Node:
    def __init__(self, depth, location, left_child, right_child):
        self.right_child = right_child
        self.left_child = left_child
        self.location = location
        self.depth = depth

    def __repr__(self):
        return pformat((self.left_child, self.to_tuple(), self.right_child))

    def to_tuple(self):
        return self.location

    def is_in_range(self, c_range):
        return c_range[0][0] <= self.location[0] <= c_range[1][0] and c_range[0][1] <= self.location[1] <= c_range[1][1]

    def range_search(self, c_range, draw):
        return self.do_range_search(c_range, [], draw)

    def do_range_search(self, c_range, points, draw):
        if self.is_in_range(c_range):
            points.append(self.location)
            draw(self.location)
            self.left_child.do_range_search(c_range, points, draw)
            self.right_child.do_range_search(c_range, points, draw)
        else:
            axis = self.depth % k

            current_cord = self.location[axis]
            range_min = c_range[0][axis]
            range_max = c_range[1][axis]

            if current_cord > range_min:
                self.left_child.do_range_search(c_range, points, draw)
            if current_cord < range_max:
                self.right_child.do_range_search(c_range, points, draw)
        return points

    def insert(self, point):
        axis = self.depth % k
        current_cord = self.location[axis]

        if point[axis] > current_cord:
            if self.right_child.is_full_node():
                self.right_child.insert(point)
            else:
                self.right_child = Node(
                    depth=self.depth + 1,
                    location=point,
                    left_child=EmptyLeaf(),
                    right_child=EmptyLeaf()
                )
        else:
            if self.left_child.is_full_node():
                self.left_child.insert(point)
            else:
                self.left_child = Node(
                    depth=self.depth + 1,
                    location=point,
                    left_child=EmptyLeaf(),
                    right_child=EmptyLeaf()
                )

    def is_full_node(self):
        return True

    def draw_rectangle(self, ax, constrains):  # left, bottom, right, up
        """Recursively plot a visualization of the KD tree region"""
        if self.depth % k == 0:
            rect = plt.Rectangle((self.location[0], constrains[1]), constrains[2] - self.location[0],
                                 constrains[3] - constrains[1], ec='k', fc='none')
            ax.add_patch(rect)
            self.left_child.draw_rectangle(ax, (constrains[0], constrains[1], self.location[0], constrains[3]))
            self.right_child.draw_rectangle(ax, (self.location[0], constrains[1], constrains[2], constrains[3]))
        else:
            rect = plt.Rectangle((constrains[0], self.location[1]), constrains[2] - constrains[0],
                                 constrains[3] - self.location[1], ec='k', fc='none')
            ax.add_patch(rect)
            self.left_child.draw_rectangle(ax, (constrains[0], constrains[1], constrains[2], self.location[1]))
            self.right_child.draw_rectangle(ax, (constrains[0], self.location[1], constrains[2], constrains[3]))


class EmptyLeaf(Node):
    def __init__(self):
        super().__init__(-1, (0, 0), self, self)

    def __repr__(self):
        return "_"

    def do_range_search(self, c_range, points, draw):
        return points

    def is_full_node(self):
        return False

    def draw_rectangle(self, ax, constrains):
        pass


def kdtree(point_list, depth=0):
    if len(point_list) == 0:
        return EmptyLeaf()
    axis = depth % k

    # Sort point list and choose median as pivot element
    point_list.sort(key=itemgetter(axis))
    median = len(point_list) // 2  # choose median

    # Create node and construct subtrees
    return Node(
        depth=depth,
        location=point_list[median],
        left_child=kdtree(point_list[:median], depth + 1),
        right_child=kdtree(point_list[median + 1:], depth + 1)
    )


def main():
    point_list = generate_in_range(0, 10, 15)
    tree = kdtree(point_list)
    print(tree)
    fig = plt.figure()
    fig.subplots_adjust(wspace=0.1, hspace=0.15,
                        left=0.1, right=0.9,
                        bottom=0.05, top=0.9)

    ax = prepare_subplot(fig, point_list, 1)
    tree.draw_rectangle(ax, (0, 0, 20, 20))
    if not draw_range:
        tree.range_search(c_range, lambda *args: None)
    else:
        rect = plt.Rectangle(c_range[0], c_range[1][0] - c_range[0][0],
                             c_range[1][1] - c_range[0][1], ec='k', fc='none', edgecolor='red', linestyle='dashed',
                             linewidth='3')
        ax.add_patch(rect)
        tree.range_search(c_range, lambda point: ax.scatter([point[0]], [point[1]], s=22, color='red'))
    fig.suptitle('$k$d-tree Example')
    plt.show()


def prepare_subplot(fig, point_list, number):
    ax = fig.add_subplot(1, 1, number)
    ax.scatter(list(map(lambda e: e[0], point_list)), list(map(lambda e: e[1], point_list)), s=9)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    return ax


if __name__ == '__main__':
    main()
