from util import *
import os
current_working_dir = os.path.dirname(os.path.realpath(__file__))
my_list = path_to_list(current_working_dir)
parent_directory = path_delimiter().join(my_list[:-1])
input_data_folder = os.path.join(*[parent_directory, "InputData"])
list_of_paths = [x.replace(input_data_folder,"") for x in get_paths_to_data_files() if path_to_list(x)[-2] != "Class"]

for x in list_of_paths:
    print(x)