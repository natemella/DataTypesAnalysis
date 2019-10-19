import os
import shutil
from DataStandardization.util import *
import argparse
import random
import itertools


def checkfile(dtype, to_combine):
    # write_dir(output_directory, INPUT_DATA, "PFI", list_of_dTypes, os.listdir(d_type_directory), Covariate_dir)

    file_name = f'{output_directory}{dtype}'
    File1 = open(f'{file_name}.txt', 'a')
    myFiles = [File1]
    if dtype in to_combine:
        return myFiles
    for i in range(0, len(to_combine)):
        file_name += f'+{to_combine[i]}'
        additional_file = open(f'{file_name}.txt', 'a')
        myFiles.append(additional_file)
    return myFiles

def match_endpoint(inputfile, endpoint):
    if inputfile.split("_")[-2] == endpoint:
        return True
    return False
def pop_back(file):
    file.close()
    with open(file.name, 'rb+') as filehandle:
        filehandle.seek(-1, os.SEEK_END)
        filehandle.truncate()
    file = open(file.name, 'a')
    return file

def get_list_of_data_paths():
    list_of_paths = get_paths_to_data_files()
    list_of_paths = [x for x in list_of_paths if
                     path_to_list(x)[-3] in list_of_cancer_types and path_to_list(x)[-2] != "Class" and path_to_list(x)[-2] != "Covariate"]
    return list_of_paths

parser = argparse.ArgumentParser(description="Develop a summary of file information and cut the file.")
parser.add_argument(
    "algorithm",
    help="which algorithm would you like to use",
)
parser.add_argument(
    "endpoints",
    help="What you would like to predict (PFI, 0S, DSS, DFI).",
    nargs='+'
)
parser.add_argument(
    "num",
    help="How many combinations",
)



args = parser.parse_args()
algorithm = args.algorithm
number_of_combinations = int(args.num)

currentWorkingDir = os.path.dirname(os.path.realpath(__file__))

RelevantTypes = ()

SEED = 448

with open("DataStandardization/CancerTypes.txt") as cancers:
    list_of_cancer_types = [cancer.strip('\n') for cancer in cancers]

list_of_cancer_types = [f'TCGA_{cancer}' for cancer in list_of_cancer_types]
random.seed(SEED)
random.shuffle(list_of_cancer_types)

list_of_cancer_types = list_of_cancer_types[7:]


remove = "True"
quick_analysis = "False"
cut_files = "False"

endpoints = args.endpoints

#
combination_list = []


output_directory = os.path.join(*[currentWorkingDir, f'Data_To_Process_Files{path_delimiter()}{algorithm}{path_delimiter()}'])

if os.path.exists(output_directory):
    shutil.rmtree(output_directory)
os.makedirs(output_directory)

INPUT_DATA = next(os.walk(currentWorkingDir + f"{path_delimiter()}InputData"))[1]

# for unix it would be '{_}' for windows it would be '\'
_=path_delimiter()

all_data_types = ["RPPA", "DNA_Methylation", "CNV", "Clinical", "SM", "Expression", "miRNA"]

cut_files = "True"

all_combos = list(itertools.combinations(all_data_types, number_of_combinations))
for combination_list in all_combos:
    for CancerType in INPUT_DATA:
        if CancerType not in list_of_cancer_types:
            continue
        for list_of_dTypes in next(os.walk(os.path.join(*[currentWorkingDir,"InputData",CancerType]))):
            if len(list_of_dTypes) > 1 and isinstance(list_of_dTypes, list):
                for DataType in list_of_dTypes:
                    list_of_dtype_dirs = [f"{currentWorkingDir}{_}InputData{_}{CancerType}{_}{data}" for data in combination_list]
                    d_type_directory = f"{currentWorkingDir}{_}InputData{_}{CancerType}{_}{DataType}"
                    if DataType != "Class" and DataType != "Covariate":
                        myFiles = checkfile(DataType, combination_list)
                        for x in endpoints:
                            names_of_input_files = ""
                            header = f'{CancerType}\t{x}\t{DataType}'
                            myFiles[0].write(f'{header}\t')
                            for input_file in os.listdir(d_type_directory):
                                if quick_analysis == "True" and not is_temp_file(input_file):
                                    continue
                                if cut_files == "True" and not is_cut_file(input_file):
                                    continue
                                if quick_analysis == "False" and cut_files == "False" and is_cut_or_tempfile(input_file):
                                    continue
                                if quick_analysis == "True" or cut_files == "True":
                                    if not match_endpoint(input_file, x):
                                        continue
                                names_of_input_files += f'{input_file},'
                            myFiles[0].write(names_of_input_files[:-1])
                            names_of_input_files = names_of_input_files[:-1] + '\t'
                            for i in range(1, len(myFiles)):
                                header += f',{combination_list[i-1]}'
                                myFiles[i].write(f'{header}\t')
                                for input_file in os.listdir(list_of_dtype_dirs[i-1]):
                                    if quick_analysis == "True" and not is_temp_file(input_file):
                                        continue
                                    if cut_files == "True" and not is_cut_file(input_file):
                                        continue
                                    if quick_analysis == "False" and cut_files == "False" and is_cut_or_tempfile(input_file):
                                        continue
                                    if quick_analysis == "True" or cut_files == "True":
                                        if not match_endpoint(input_file, x):
                                            continue
                                    names_of_input_files += f'{input_file},'
                                myFiles[i].write(names_of_input_files[:-1])
                                names_of_input_files = names_of_input_files[:-1] + '\t'
                            for file in myFiles:
                                file.write('\n')
                        for x in myFiles:
                            x.close()
    if len(combination_list) == 0:
        remove = "False"
    if remove == "True":
        for input_file in os.listdir(output_directory):
            if len(input_file.split('+')) < 2:
                os.remove(os.path.join(*[output_directory, input_file]))
                continue
            last_dtype = input_file.split('+')[-1]
            if last_dtype.split('.')[0] != combination_list[-1]:
                os.remove(os.path.join(*[output_directory, input_file]))






