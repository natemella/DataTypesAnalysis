import os
import sys
import shutil
currentWorkingDir = os.path.dirname(os.path.realpath(__file__))

RelevantTypes = ()

def path_to_list(path):
  folders = []
  while True:
    path, folder = os.path.split(path)
    if folder:
      folders.append(folder)
    else:
      if path:
        folders.append(path)
      break
  folders.reverse()
  return folders

def sep_maker():
  list = ['a','b']
  x = os.path.join(*list)
  return x[1]





endpoints = sys.argv[1:]


my_list = path_to_list(currentWorkingDir)
parent_directory = sep_maker().join(my_list[:-1])

INPUT_DATA = next(os.walk(parent_directory + f"{sep_maker()}InputData"))[1]

# for unix it would be '{_}' for windows it would be '\'
_=sep_maker()


for CancerType in INPUT_DATA:
    for list_of_dTypes in next(os.walk(os.path.join(*[parent_directory,"InputData",CancerType]))):
        if len(list_of_dTypes) > 1 and isinstance(list_of_dTypes, list):
            for DataType in list_of_dTypes:
                d_type_directory = f"{parent_directory}{_}InputData{_}{CancerType}{_}{DataType}"
                if DataType != "Class":
                    for input_file in os.listdir(d_type_directory):
                        input_file = f'{d_type_directory}{_}{input_file}'
                        if input_file.endswith(('.tsv','.txt')):
                            num_Patients = sum(1 for line in open(input_file))
                        else:
                            with open(input_file) as myfile:
                                num_Patients = len(myfile.readline().split('\t'))
                        if num_Patients < 100:
                            print(f'{CancerType} {DataType} Number of Patients == {num_Patients}')

