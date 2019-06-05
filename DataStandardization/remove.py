import os
import shutil
from util import *

current_working_dir = os.path.dirname(os.path.realpath(__file__))
relevant_types = make_relevant_types_list()
abbreviations_dict = make_abbrevation_dict(relevant_types)
folders_list = path_to_list(current_working_dir)
parent_directory = path_delimiter().join(folders_list[:-1])

_= path_delimiter()

# need to invert dictionary

abbreviations_dict = {value: key for key, value in abbreviations_dict.items()} # reverse keys and values

for x in next(os.walk(f'{parent_directory}{_}InputData'))[1]:
    if x.split('_')[1] not in abbreviations_dict:
        shutil.rmtree(f'{parent_directory}{_}InputData{_}{x}')
        print(x)
