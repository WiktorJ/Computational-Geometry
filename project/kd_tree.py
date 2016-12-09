from operator import itemgetter
from pprint import pformat
from matplotlib import pyplot as plt

from generator_utils import generate_in_range
from project.draw_utils import prepare_subplot, get_draw_point

k = 2
lims = (0, 10)
c_range = ((3, 5), (8, 9))
draw_range = True
frame_time = 0.0001
step_draw = True
points_number = 10



class Node:
    """
    Class that represents single node of tree.
    """
    def __init__(self, depth, location, left_child, right_child, constrains_left, constrains_right):
        """
        :param self.constrains_right: Rectangle that defines area for the right child to divide
        :param self.constrains_left: Rectangle that defines area for the left child to divide
        :param self.right_child:
        :param self.left_child:
        :param self.location: Point that node represents
        :param self.depth:
        """
        self.constrains_right = constrains_right
        self.constrains_left = constrains_left
        self.right_child = right_child
        self.left_child = left_child
        self.location = location
        self.depth = depth

    def __repr__(self):
        return pformat((self.left_child, self.to_tuple(), self.right_child))

    def to_tuple(self):
        return self.location

    def is_in_range(self, c_range):
        """
        Checks if given node is in c_range
        :param c_range:
        :return: boolean value
        """
        return c_range[0][0] <= self.location[0] <= c_range[1][0] and c_range[0][1] <= self.location[1] <= c_range[1][1]

    def range_search(self, c_range, draw):
        """
        For user to start range search
        :param c_range:
        :param draw: Function that is called every time new point is classified in c_range
        :return: List of classified points
        """
        return self.do_range_search(c_range, [], draw)

    def do_range_search(self, c_range, points, draw):
        """
        Actual range search function
        :param c_range:
        :param points: So far classified points
        :param draw:
        :return:
        """
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

    def insert(self, point, draw):
        """
        Recursively insert point to the tree
        :param point: Point to insert
        :param draw: Function that is called every time new point is inserted to draw division on the plot. It
            takes coordinates of outer rectangle point to draw and its axis (x=0 or y=1)
        :return:
        """
        axis = self.depth % k
        child_axis = (self.depth + 1) % k
        current_cord = self.location[axis]

        if point[axis] > current_cord:
            if self.right_child.is_full_node():
                self.right_child.insert(point, draw)
            else:
                draw(self.constrains_right, point, child_axis)
                self.right_child = create_node(point, self.depth + 1, self.constrains_right, child_axis)
        else:
            if self.left_child.is_full_node():
                self.left_child.insert(point, draw)
            else:
                draw(self.constrains_left, point, child_axis)
                self.left_child = create_node(point, self.depth + 1, self.constrains_left, child_axis)

    def is_full_node(self):
        """
        Check if node is regular node.
        :return: Always true.
        """
        return True


class EmptyLeaf(Node):
    """
    Class representing empty node. Created for implementation simplification.
    """
    def __init__(self):
        super().__init__(-1, (0, 0), self, self, (0, 0, 0, 0), (0, 0, 0, 0))

    def __repr__(self):
        return "_"

    def do_range_search(self, c_range, points, draw):
        return points

    def is_full_node(self):
        return False

    def draw_rectangle(self, ax, constrains):
        pass


def create_node(location, depth, constrains, axis):
    """
    Helper function for creating node.
    :param location:
    :param depth:
    :param constrains:
    :param axis:
    :return:
    """
    return Node(
        depth=depth,
        location=location,
        left_child=EmptyLeaf(),
        right_child=EmptyLeaf(),
        constrains_left=(constrains[0], constrains[1], location[0], constrains[3]) if axis == 0 else (
            constrains[0], constrains[1], constrains[2], location[1]),
        constrains_right=(location[0], constrains[1], constrains[2], constrains[3]) if axis == 0 else (
            constrains[0], location[1], constrains[2], constrains[3])
    )


def get_draw(ax):
    """
    :param ax: Subplot
    :return: Functions that draws rectangle on given subplot
    """
    def draw_rectangle(constrains, location, axis):  # left, bottom, right, up
        """
        Draw rectangle
        :param constrains: Parent constrains/
        :param location: Point which is dividing space
        :param axis:
        :return:
        """
        if axis % k == 0:
            rect = plt.Rectangle((location[0], constrains[1]), constrains[2] - location[0],
                                 constrains[3] - constrains[1], ec='k', fc='none')
            draw_rect(ax, rect)
        else:
            rect = plt.Rectangle((constrains[0], location[1]), constrains[2] - constrains[0],
                                 constrains[3] - location[1], ec='k', fc='none')
            draw_rect(ax, rect)

    return draw_rectangle


def draw_rect(ax, rect):
    """
    Draw rectangle
    :param ax: subplot
    :param rect: plt.Rectangle element.
    :return:
    """
    ax.add_patch(rect)
    plt.draw()
    plt.pause(frame_time)
    if step_draw:
        input("Press [enter] to continue.")


def kdtree(point_list, draw, ax):
    """
    Creates kdtree by inserting all points
    :param point_list:
    :param draw:
    :param ax:
    :return: kdtree
    """
    draw_current_point = get_draw_point(ax, plt, frame_time, step_draw, 32, 'green')
    tree = Node(0, point_list[0], EmptyLeaf(), EmptyLeaf(), (lims[0], lims[0], point_list[0][0], lims[1]),
                (point_list[0][0], lims[0], lims[1], lims[1]))
    draw((lims[0], lims[0], lims[1], lims[1]), point_list[0], 0)
    for point in point_list[1:]:
        current_point = draw_current_point(point)
        tree.insert(point, draw)
        current_point.remove()
    return tree

def kdtree2(point_list, depth=0):
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
        left_child=kdtree2(point_list[:median], depth + 1),
        right_child=kdtree2(point_list[median + 1:], depth + 1)
    )



def main():
    point_list = generate_in_range(lims[0], lims[1], points_number)
    # point_list = sorted(point_list)
    # point_list = list(map(lambda t: (float(t[0]), float(t[1])), read_file_to_tuples('points.csv')))
    # write_tuple_to_file("points.csv", point_list)
    # point_list = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2)]
    plt.ion()
    plt.show()
    fig = plt.figure()
    fig.subplots_adjust(wspace=0.1, hspace=0.15,
                        left=0.1, right=0.9,
                        bottom=0.05, top=0.9)

    ax = prepare_subplot(fig, point_list, 1, 1, 1, lims)
    tree = kdtree(point_list, get_draw(ax), ax)
    if not draw_range:
        tree.range_search(c_range, lambda *args: None)
    else:
        rect = plt.Rectangle(c_range[0], c_range[1][0] - c_range[0][0],
                             c_range[1][1] - c_range[0][1], ec='k', fc='none', edgecolor='red', linestyle='dashed',
                             linewidth='3')
        ax.add_patch(rect)

        input("Press [enter] to search.")
        tree.range_search(c_range, get_draw_point(ax, plt, frame_time, step_draw, 22, 'red'))
    input("Press [enter] to finish.")
    plt.show()


if __name__ == '__main__':
    main()
