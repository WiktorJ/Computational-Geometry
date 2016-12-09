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


def remove_characters(path, to_remove):
    split_path = path.split('.')
    out_path = split_path[0] + '_new.csv'
    with open(path, 'r') as infile, open(out_path, 'w') as outfile:
        data = infile.read()
        for char in to_remove:
            data = data.replace(char, '')
        outfile.write(data)
    return out_path



