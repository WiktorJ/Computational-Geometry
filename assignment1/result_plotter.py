import matplotlib.pyplot as plt
import csv


def plot(left, right, on, i, j):
    # pass
    fig = plt.figure(1)
    ax = fig.add_subplot(111, axisbg='black')
    if left:
        ax.scatter(*zip(*left), color='white', label='left')
    if right:
        ax.scatter(*zip(*right), color='red', label='right')
    if on:
        ax.scatter(*zip(*on), color='green', label='on')
    legend = plt.legend(loc=2)
    frame = legend.get_frame()
    frame.set_facecolor('blue')
    frame.set_edgecolor('grey')
    fig.canvas.draw()
    # plt.savefig('epsilon12/{i!s}_{j!s}.png'.format(**locals()), bbox_inches='tight')
    plt.show()
    fig.clf()


def read_file_to_tuples(path):
    print('opening file', path)
    with open(path) as the_file:
        return [tuple(line) for line in csv.reader(the_file, delimiter=" ")]

for i in range(4, 5):
    for j in range(0, 5):
        plot(read_file_to_tuples('epsilon0/{i!s}_{j!s}_l.csv'.format(**locals())),
             read_file_to_tuples('epsilon0/{i!s}_{j!s}_r.csv'.format(**locals())),
             read_file_to_tuples('epsilon0/{i!s}_{j!s}_o.csv'.format(**locals())), i, j)
