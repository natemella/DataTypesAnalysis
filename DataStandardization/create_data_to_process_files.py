import os
import pandas as pd

currentWorkingDir = os.path.dirname(os.path.realpath(__file__))

RelevantTypes = ()

DataTypes = ("SM, RPPA, miRNA, Covariate, CNV")

endpoints = ("DFI, PFI, DSS, OS")

def write_dir(InputData, endpoint):
    for x in DataTypes:
        with open(f'{x}.txt', 'w+') as newFile:
            write_file(InputData, newFile, combined=False, endpoint=endpoint)
        if x != "Covariate":
            with open(f'{x}_and_Covariate.txt', 'w+') as newFile:
                write_file(InputData, newFile, combined=True, endpoint=endpoint)


def write_file(InputData, File, combined, endpoint):

    if not combined:
        dataType = File.name.split('.')[0]
        File.write(f'#Cancer_Type\tClass\tDataTypes\tFiles_For_{dataType}\n')
        for cancerType in InputData:
            for x in endpoints:
                if x != endpoint:
                    File.write('#')
                File.write(f'{cancerType}\t{x}\t{dataType}')
                for input_file in cancerType:
                    File.write(f'\t{input_file}')
                File.write('\n')
        return
    else:
        dataTypes = File.name.split('.')[0]
        dataType_1 = dataTypes.split('_')[0]
        dataType_2 = dataTypes.split('_')[2]
        File.write(f'#Cancer_Type\tClass\tDataTypes\tFiles_For_{dataType_1}\tFiles_For_{dataType_2}\n')
        for cancerType in InputData:
            for x in endpoints:
                if x != endpoint:
                    File.write('#')
                File.write(f'{cancerType}\t{x}\t{dataType_1},{dataType_2}')
                for input_file in cancerType:
                    File.write(f'\t{input_file}')
                File.write('\n')



list = currentWorkingDir.split('/')
parent_directory = '/'.join(list[:-1])


endpoints = ("DFI","DSS","OS","PFI")


for x in next(os.walk(parent_directory + "/InputData"))[1]:
    for subdir in next(os.walk(parent_directory + "/InputData/" + x)):
        if "Covariate" in subdir:
            directory = f"{parent_directory}/InputData/{x}/Covariate"
            for filename in os.listdir(directory):
                if filename.endswith(".tsv"):
                    Class_dir = f"{parent_directory}/InputData/{x}/Class/"
                    if not os.path.exists(os.path.dirname(Class_dir)):
                        os.makedirs(os.path.dirname(Class_dir))
                    #separate endpoints. Build df of just endpoint + endpoint.time

                else:
                    continue



