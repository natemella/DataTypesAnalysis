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


def checkfunction(dtype):
    # write_dir(output_directory, INPUT_DATA, "PFI", list_of_dTypes, os.listdir(d_type_directory), Covariate_dir)
    if not os.path.exists(os.path.dirname(f'{output_directory}{_}{dtype}.txt')):
        File1 = open(f'{output_directory}{_}{dtype}.txt', 'w+')
    else:
        File1 = open(f'{output_directory}{_}{dtype}.txt', 'a')

    if dtype != "Covariate":
        if not os.path.exists(os.path.dirname(f'{output_directory}{_}{dtype}_and_Covariate.txt')):
            File2 = open(f'{output_directory}{_}{dtype}_and_Covariate.txt', 'w+')
        else:
            File2 = open(f'{output_directory}{_}{dtype}_and_Covariate.txt', 'a')
        return [File1, File2]
    else:
        return [File1]


def pop_back(file):
    file.close()
    with open(file.name, 'rb+') as filehandle:
        filehandle.seek(-1, os.SEEK_END)
        filehandle.truncate()
    file = open(file.name, 'a')
    return file

endpoints = sys.argv[1:]


my_list = path_to_list(currentWorkingDir)
parent_directory = sep_maker().join(my_list[:-1])
output_directory = os.path.join(*[parent_directory,f'Data_To_Process_Files{sep_maker()}'])
if not os.path.exists(os.path.dirname(output_directory)):
    os.makedirs(os.path.dirname(output_directory))
else:
    shutil.rmtree(os.path.dirname(output_directory))
    os.makedirs(os.path.dirname(output_directory))

INPUT_DATA = next(os.walk(parent_directory + f"{sep_maker()}InputData"))[1]

# for unix it would be '{_}' for windows it would be '\'
_=sep_maker()


for CancerType in INPUT_DATA:
    for list_of_dTypes in next(os.walk(os.path.join(*[parent_directory,"InputData",CancerType]))):
        if len(list_of_dTypes) > 1 and isinstance(list_of_dTypes, list):
            for DataType in list_of_dTypes:
                d_type_directory = f"{parent_directory}{_}InputData{_}{CancerType}{_}{DataType}"
                Covariate_dir = f"{parent_directory}{_}InputData{_}{CancerType}{_}Covariate{_}"
                if DataType != "Class":
                    myFiles = checkfunction(DataType)
                    if DataType == "Covariate":
                        # combined = False
                        for x in endpoints:
                            myFiles[0].write(f'{CancerType}\t{x}\t{DataType}\t')
                            for input_file in os.listdir(d_type_directory):
                                if input_file.endswith('.tsv'):
                                    continue
                                myFiles[0].write(f'{input_file},')
                            myFiles[0] = pop_back(myFiles[0])
                            myFiles[0].write('\n')
                        myFiles[0].close()
                    else:
                        # combined = True
                        for x in endpoints:
                            myFiles[1].write(f'{CancerType}\t{x}\t{DataType},Covariate\t')
                            for input_file in os.listdir(d_type_directory):
                                myFiles[1].write(f'{input_file},')
                            myFiles[1] = pop_back(myFiles[1])
                            myFiles[1].write('\t')
                            for input_file in os.listdir(Covariate_dir):
                                if input_file.endswith('.tsv'):
                                    continue
                                myFiles[1].write(f'{input_file},')
                            myFiles[1] = pop_back(myFiles[1])
                            myFiles[1].write('\n')
                        for x in endpoints:
                            myFiles[0].write(f'{CancerType}\t{x}\t{DataType}\t')
                            for input_file in os.listdir(d_type_directory):
                                myFiles[0].write(f'{input_file},')
                            myFiles[0] = pop_back(myFiles[0])
                            myFiles[0].write('\n')
                        myFiles[0].close()
                        myFiles[1].close()








