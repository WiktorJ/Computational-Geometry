import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import csv


def plot(points):
    plt.scatter(*zip(*points))
    plt.show()

def plot3d(points):
    print("plottinh")
    X, Y, Z = list(zip(*points))
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_trisurf(X, Y, Z)
    plt.show()


def read_file_to_tuples(path):
    with open(path) as the_file:
        return [tuple(line) for line in csv.reader(the_file, delimiter=" ")]


plot3d(read_file_to_tuples('out1.txt'))
# plot(read_file_to_tuples('data_set_1.csv'))
# plot(read_file_to_tuples('data_set_2.csv'))
# plot(read_file_to_tuples('data_set_3.csv'))
# plot(read_file_to_tuples('data_set_4.csv'))
