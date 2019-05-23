import os
import sys
import shutil
currentWorkingDir = os.path.dirname(os.path.realpath(__file__))

RelevantTypes = ()


def checkfunction(dtype):
    # write_dir(output_directory, INPUT_DATA, "PFI", list_of_dTypes, os.listdir(d_type_directory), Covariate_dir)
    if not os.path.exists(os.path.dirname(f'{output_directory}/{dtype}.txt')):
        File1 = open(f'{output_directory}/{dtype}.txt', 'w+')
    else:
        File1 = open(f'{output_directory}/{dtype}.txt', 'a')

    if dtype != "Covariate":
        if not os.path.exists(os.path.dirname(f'{output_directory}/{dtype}_and_Covariate.txt')):
            File2 = open(f'{output_directory}/{dtype}_and_Covariate.txt', 'w+')
        else:
            File2 = open(f'{output_directory}/{dtype}_and_Covariate.txt', 'a')
        return [File1, File2]
    else:
        return [File1]




endpoints = sys.argv[1:]


my_list = currentWorkingDir.split('/')
parent_directory = '/'.join(my_list[:-1])
output_directory = f'{parent_directory}/Data_To_Process_Files/'
if not os.path.exists(os.path.dirname(output_directory)):
    os.makedirs(os.path.dirname(output_directory))
else:
    shutil.rmtree(os.path.dirname(output_directory))
    os.makedirs(os.path.dirname(output_directory))

INPUT_DATA = next(os.walk(parent_directory + "/InputData"))[1]

for CancerType in next(os.walk(parent_directory + "/InputData"))[1]:
    for list_of_dTypes in next(os.walk(parent_directory + "/InputData/" + CancerType)):
        if len(list_of_dTypes) > 1 and isinstance(list_of_dTypes, list):
            for DataType in list_of_dTypes:
                d_type_directory = f"{parent_directory}/InputData/{CancerType}/{DataType}"
                Covariate_dir = f"{parent_directory}/InputData/{CancerType}/Covariate/"
                if DataType != "Class":
                    myFiles = checkfunction(DataType)
                    if DataType == "Covariate":
                        # combined = False
                        for x in endpoints:
                            myFiles[0].write(f'{CancerType}\t{x}\t{DataType}')
                            for input_file in os.listdir(d_type_directory):
                                if input_file.endswith('.tsv'):
                                    continue
                                myFiles[0].write(f'\t{input_file}')
                            myFiles[0].write('\n')
                        myFiles[0].close()
                    else:
                        # combined = True
                        for x in endpoints:
                            myFiles[1].write(f'{CancerType}\t{x}\t{DataType},Covariate')
                            for input_file in os.listdir(d_type_directory):
                                myFiles[1].write(f'\t{input_file}')
                            for input_file in os.listdir(Covariate_dir):
                                myFiles[1].write(f'\t{input_file}')
                            myFiles[1].write('\n')
                        myFiles[0].close()
                        myFiles[1].close()








