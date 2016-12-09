
def prepare_subplot(fig, point_list, cols, rows, number, lims):
    """
    This method prepares plot for futher animation.
    :param fig: Figure from pyplot ( fig = plt.figure())
    :param point_list: Points to draw on the subplot
    :param cols: On how many columns should plot be divided
    :param rows: On how many rows should plot be divided
    :param number: Number of subplots
    :param lims: Limits of axis
    :return:
    """
    ax = fig.add_subplot(cols, rows, number)
    ax.scatter(list(map(lambda e: e[0], point_list)), list(map(lambda e: e[1], point_list)), s=9)
    ax.set_xlim(lims[0], lims[1])
    ax.set_ylim(lims[0], lims[1])
    return ax


def get_draw_point(ax, plt, frame_time, step_draw, size, color):
    """
    :param ax: Subplot to draw on
    :param plt: Pyplot variable
    :param frame_time: For how long should be frame visible
    :param step_draw: Wait for key press to step to next frame
    :param size: Size of point
    :param color: Color of point
    :return: Function that draws point according to arguments specified in outter function
    """
    def draw_point(point):
        """
        :param point: Point to draw
        :return: Reference to point (eg. for removing it)
        """
        point = ax.scatter([point[0]], [point[1]], s=size, color=color)
        plt.draw()
        plt.pause(frame_time)
        if step_draw:
            input("Press [enter] to continue (POINT).")
        return point

    return draw_point
