import random
import math
import csv


def get_random(min, max):
    return random.uniform(min, max)


def generate_in_range(min, max, amount):
    points = []
    for _ in range(0, amount):
        points.append((get_random(min, max), get_random(min, max)))
    return points


def generate_on_circle(center_x, center_y, radius, amount):
    points = []
    for _ in range(0, amount):
        angle = get_random(0, 2 * math.pi)
        points.append((center_x + radius * math.cos(angle), center_y + radius * math.sin(angle)))
    return points


def generate_on_line(min, max, amount):
    points = []
    for _ in range(0, amount):
        x = get_random(min, max)
        points.append((x, 0.05 * x + 0.05))
    return points


def write_tuple_to_file(path, tuples):
    with open(path, "w") as the_file:
        csv.register_dialect("custom", delimiter=" ", skipinitialspace=True)
        writer = csv.writer(the_file, dialect="custom")
        for tup in tuples:
            writer.writerow(tup)


write_tuple_to_file("data_set_1.csv", generate_in_range(-100, 100, 100))
# write_tuple_to_file("data_set_2.csv", generate_in_range(-1e14, 1e14, 100000))
write_tuple_to_file("data_set_3.csv", generate_on_circle(0, 0, 10, 100))
# write_tuple_to_file("data_set_4.csv", generate_on_line(-1e3, 1e3, 1000))
