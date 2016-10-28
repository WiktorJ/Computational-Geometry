from custom_file_utils import write_tuple_to_file
from generator_utils import generate_in_range, generate_on_circle, generate_on_line

write_tuple_to_file("data_set_1.csv", generate_in_range(-1e2, 1e2, 100000))
write_tuple_to_file("data_set_2.csv", generate_in_range(-1e14, 1e14, 100000))
write_tuple_to_file("data_set_3.csv", generate_on_circle(0, 0, 1e2, 1000))
write_tuple_to_file("data_set_4.csv", generate_on_line(-1e3, 1e3, 1000))
