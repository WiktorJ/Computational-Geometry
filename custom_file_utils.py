import csv
import os
from shutil import copyfile


def write_tuple_to_file(path, tuples):
    if os.path.dirname(path) != '':
        os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as the_file:
        csv.register_dialect("custom", delimiter=" ", skipinitialspace=True)
        writer = csv.writer(the_file, dialect="custom")
        for tup in tuples:
            writer.writerow(tup)


def read_file_to_tuples(path, delimiter=" "):
    print('opening file', path)
    with open(path) as the_file:
        return [tuple(line) for line in csv.reader(the_file, delimiter=delimiter)]


def copy_file(source, destination):
    if os.path.dirname(destination) != '':
        os.makedirs(os.path.dirname(destination), exist_ok=True)
    copyfile(source, destination)
