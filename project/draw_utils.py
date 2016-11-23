def prepare_subplot(fig, point_list, cols, rows, number):
    ax = fig.add_subplot(cols, rows, number)
    ax.scatter(list(map(lambda e: e[0], point_list)), list(map(lambda e: e[1], point_list)), s=9)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    return ax