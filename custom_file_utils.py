import csv
import os


def write_tuple_to_file(path, tuples):
    if os.path.dirname(path) != '':
        os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as the_file:
        csv.register_dialect("custom", delimiter=" ", skipinitialspace=True)
        writer = csv.writer(the_file, dialect="custom")
        for tup in tuples:
            print(tup)
            writer.writerow(tup)


def read_file_to_tuples(path):
    print('opening file', path)
    with open(path) as the_file:
        return [tuple(line) for line in csv.reader(the_file, delimiter=" ")]
