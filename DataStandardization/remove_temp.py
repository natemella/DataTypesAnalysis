from util import *
import os

def is_temp_file(input_file):
    folders = path_to_list(input_file)
    checking = folders[-1].split("_")
    if checking[-1].split('.')[0] == "temp":
        return True
    return False

current_working_dir = os.path.dirname(os.path.realpath(__file__))
my_list = path_to_list(current_working_dir)
parent_directory = path_delimiter().join(my_list[:-1])
input_data_folder = os.path.join(*[parent_directory, "InputData"])
list_of_paths = [x for x in get_paths_to_data_files() if is_temp_file(x)]

for x in list_of_paths:
    print(x)
    os.remove(x)