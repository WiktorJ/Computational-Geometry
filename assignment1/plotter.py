import matplotlib.pyplot as plt
import csv


# N = 50
# x = np.random.rand(N)
# y = np.random.rand(N)
#
# plt.scatter(x, y)
# plt.show()

def plot(points):
    plt.scatter(*zip(*points))
    plt.show()


def read_file_to_tuples(path):
    with open(path) as the_file:
        return [tuple(line) for line in csv.reader(the_file, delimiter=" ")]


plot(read_file_to_tuples('data_set_1.csv'))
plot(read_file_to_tuples('data_set_2.csv'))
plot(read_file_to_tuples('data_set_3.csv'))
plot(read_file_to_tuples('data_set_4.csv'))
