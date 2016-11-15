from custom_file_utils import write_tuple_to_file
from generator_utils import generate_in_range, generate_on_circle, generate_on_quadrangle, \
    generate_on_square

write_tuple_to_file("data_set_1.csv", generate_in_range(-100, 100, 100000))
write_tuple_to_file("data_set_2.csv", generate_on_circle(0, 0, 10, 100))
write_tuple_to_file("data_set_3.csv", generate_on_quadrangle((-10, 10), (-10, -10), (10, -10), (10, 10), 100000))
write_tuple_to_file("data_set_4.csv", generate_on_square((0, 10), (0, 0), (10, 0), (10, 10), 20000, 25000))