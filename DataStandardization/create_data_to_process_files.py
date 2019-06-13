import os
import shutil
from util import *
import argparse
import random


def checkfile(dtype):
    # write_dir(output_directory, INPUT_DATA, "PFI", list_of_dTypes, os.listdir(d_type_directory), Covariate_dir)
    if not os.path.exists(os.path.dirname(f'{output_directory}{_}{dtype}.txt')):
        File1 = open(f'{output_directory}{_}{dtype}.txt', 'w+')
    else:
        File1 = open(f'{output_directory}{_}{dtype}.txt', 'a')
    return [File1]
    # if dtype != "Covariate":
    #     if not os.path.exists(os.path.dirname(f'{output_directory}{_}{dtype}_and_Covariate.txt')):
    #         File2 = open(f'{output_directory}{_}{dtype}_and_Covariate.txt', 'w+')
    #     else:
    #         File2 = open(f'{output_directory}{_}{dtype}_and_Covariate.txt', 'a')
    #     return [File1, File2]
    # else:
    #     return [File1]


def pop_back(file):
    file.close()
    with open(file.name, 'rb+') as filehandle:
        filehandle.seek(-1, os.SEEK_END)
        filehandle.truncate()
    file = open(file.name, 'a')
    return file

parser = argparse.ArgumentParser(description="Develop a summary of file information and cut the file.")
parser.add_argument(
    "endpoints",
    help="What you would like to predict (PFI, 0S, DSS, DFI)."
)
parser.add_argument(
    "-c",
    "--covariate",
    type=str,
    default="False",
    help="bool on whether to combine all data types with covariate"
)
parser.add_argument(
    "-m",
    '--miRNA',
    type=str,
    default="False",
    help="bool on whether to combine all data types with covariate."
)
parser.add_argument(
    "-n",
    '--CNV',
    type=str,
    default="False",
    help="bool on whether to combine all data types with CNV"
)
parser.add_argument(
    "-d",
    '--DNA-Methylation',
    type=str,
    default="False",
    help="bool on whether to combine all data types with DNA methylation"
)
parser.add_argument(
    "-e",
    '--Expression',
    type=str,
    default="False",
    help="bool on whether to combine all data types with RNA Expression"
)
parser.add_argument(
    "-p",
    '--RPPA',
    type=str,
    default="False",
    help="bool on whether to combine all data types with protein expression"
)
parser.add_argument(
    "-s",
    '--Somatic-Mutations',
    type=str,
    default="False",
    help="bool on whether to combine all data types with somatic mutations"
)
parser.add_argument(
    "-q",
    '--quick-analysis',
    type=str,
    default="False",
    help="bool on whether to do 3 feature quick analysis"
)
parser.add_argument(
    "-x",
    '--cut-files',
    type=str,
    default="False",
    help="bool on whether to do analysis on cut_files"
)



args = parser.parse_args()
covariate=args.covariate
miRNA=args.miRNA
cnv=args.CNV
dna_meth = args.DNA_Methylation
expression = args.Expression
protein_expression = args.RPPA
sm = args.Somatic_Mutations
quick_analysis = args.quick_analysis
cut_files = args.cut_files

currentWorkingDir = os.path.dirname(os.path.realpath(__file__))

RelevantTypes = ()

SEED = 448

with open("CancerTypes.txt") as cancers:
    list_of_cancer_types = [cancer.strip('\n') for cancer in cancers]

list_of_cancer_types = [f'TCGA_{cancer}' for cancer in list_of_cancer_types]
random.seed(SEED)
random.shuffle(list_of_cancer_types)

list_of_cancer_types = list_of_cancer_types[0:8]

print(list_of_cancer_types)

parameters = {"covariate":covariate,"miRNA": miRNA, "cnv":cnv,
              "dna_meth":dna_meth,"expression": expression,
              "protein_expression":protein_expression, "sm":sm}

endpoints = [args.endpoints]
print(parameters)
print(f'endpoints are {endpoints}')


my_list = path_to_list(currentWorkingDir)
parent_directory = path_delimiter().join(my_list[:-1])
output_directory = os.path.join(*[parent_directory, f'Data_To_Process_Files{path_delimiter()}'])
if not os.path.exists(os.path.dirname(output_directory)):
    os.makedirs(os.path.dirname(output_directory))
else:
    shutil.rmtree(os.path.dirname(output_directory))
    os.makedirs(os.path.dirname(output_directory))

INPUT_DATA = next(os.walk(parent_directory + f"{path_delimiter()}InputData"))[1]

# for unix it would be '{_}' for windows it would be '\'
_=path_delimiter()


for CancerType in INPUT_DATA:
    if CancerType not in list_of_cancer_types:
        continue
    for list_of_dTypes in next(os.walk(os.path.join(*[parent_directory,"InputData",CancerType]))):
        if len(list_of_dTypes) > 1 and isinstance(list_of_dTypes, list):
            for DataType in list_of_dTypes:
                d_type_directory = f"{parent_directory}{_}InputData{_}{CancerType}{_}{DataType}"
                combined_dir = f"{parent_directory}{_}InputData{_}{CancerType}{_}Covariate{_}"
                if DataType != "Class":
                    myFiles = checkfile(DataType)
                    if DataType == "Covariate":
                        # combined = False
                        for x in endpoints:
                            seen_files = 0
                            myFiles[0].write(f'{CancerType}\t{x}\t{DataType}\t')
                            for input_file in os.listdir(d_type_directory):
                                if quick_analysis == "True" and not is_temp_file(input_file):
                                    continue
                                if cut_files == "True" and not is_cut_file(input_file):
                                    continue
                                if quick_analysis == "False" and cut_files == "False" and is_cut_or_tempfile(input_file):
                                    continue
                                myFiles[0].write(f'{input_file},')
                                seen_files +=1
                            myFiles[0] = pop_back(myFiles[0])
                            myFiles[0].write('\n')
                        myFiles[0].close()
                    else:
                        # combined = True
                        # for x in endpoints:
                        # myFiles[1].write(f'{CancerType}\t{x}\t{DataType},Covariate\t')
                        # for input_file in os.listdir(d_type_directory):
                        #     myFiles[1].write(f'{input_file},')
                        # myFiles[1] = pop_back(myFiles[1])
                        # myFiles[1].write('\t')
                        # for input_file in os.listdir(combined_dir):
                        #     if input_file.endswith('.tsv'):
                        #         continue
                        #     myFiles[1].write(f'{input_file},')
                        # myFiles[1] = pop_back(myFiles[1])
                        # myFiles[1].write('\n')
                        for x in endpoints:
                            myFiles[0].write(f'{CancerType}\t{x}\t{DataType}\t')
                            for input_file in os.listdir(d_type_directory):
                                if quick_analysis == "True" and not is_temp_file(input_file):
                                    continue
                                if cut_files == "True" and not is_cut_file(input_file):
                                    continue
                                if quick_analysis == "False" and cut_files == "False" and is_cut_or_tempfile(input_file):
                                    continue
                                myFiles[0].write(f'{input_file},')
                            myFiles[0] = pop_back(myFiles[0])
                            myFiles[0].write('\n')
                        myFiles[0].close()
                        # myFiles[1].close()








