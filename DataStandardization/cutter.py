import os
import pandas as pd
import codecs
from util import *
import argparse

def run_make_df_function(d_type_path, patients_with_all, DataType, quick_analysis, endpoint):
        if DataType == "Class":
            return
        for input_file in os.listdir(d_type_path):
            if is_cut_or_tempfile(input_file):
                continue
            input_file = f'{d_type_path}{_}{input_file}'
            make_df(patients_with_all, DataType, input_file, quick_analysis, endpoint)

def make_df(patient_ids, DataType, input_file, mini, endpoint):
    if input_file.endswith(".ttsv"):
        df = filter_cols(input_file, patient_ids, mini)
    else:
        if DataType != "DNA_Methylation":
            index_name = "SampleID"
        else:
            index_name = "Patient_ID"
        df = filter_rows(input_file,patient_ids, index_name, mini)
    write_file(df, mini, input_file, endpoint)


def filter_cols(input_file, patient_ids, mini):
    my_cols = list(patient_ids)
    my_cols.insert(0,"SampleID")
    my_list = [line.split('\t')[0] for line in open(input_file)]
    print(input_file)
    print(len(open(input_file).readlines()))
    print(my_list[0:10])
    df = pd.read_csv(input_file, delimiter='\t',
                       na_values='NA', usecols=my_cols, index_col="SampleID")
    print(input_file)
    print(len(df.index.values))
    print(df.index.values[0:10])
    if mini == "True":
        df = df.iloc[:3]
    return df

def filter_rows(input_file, patient_ids, index_name, mini):
    iter_csv = pd.read_csv(input_file, delimiter='\t', iterator=True, chunksize=1000)
    df = pd.concat([chunk[chunk[index_name].isin(patient_ids)] for chunk in iter_csv])
    df = df.set_index(index_name)
    if mini == "True":
        df = df.iloc[:,0:3]
    return df

def build_temp_extension(input_file, endpoint):
    if input_file.endswith(".ttsv"):
        temp_extension = f"_{endpoint}_temp.ttsv"
    elif input_file.endswith(".tsv"):
        temp_extension = f"_{endpoint}_temp.tsv"
    else:
        temp_extension = f"_{endpoint}_temp.txt"
    return temp_extension

def build_cut_extension(input_file, endpoint):
    if input_file.endswith(".ttsv"):
        cut_extension = f"_{endpoint}_cut.ttsv"
    elif input_file.endswith(".tsv"):
        cut_extension = f"_{endpoint}_cut.tsv"
    else:
        cut_extension = f"_{endpoint}_cut.txt"
    return cut_extension

def get_current_extension(input_file):
    return f".{input_file.split('.')[-1]}"

def get_new_file_path(input_file, mini, endpoint):
    current_extenstion = get_current_extension(input_file)
    if mini == "True":
        temp_extension = build_temp_extension(input_file, endpoint)
        return input_file.replace(current_extenstion, temp_extension)
    else:
        cut_extension =build_cut_extension(input_file, endpoint)
        return input_file.replace(current_extenstion, cut_extension)

def write_file(df, mini, input_file, endpoint):
    new_file_path = get_new_file_path(input_file, mini, endpoint)
    if mini == "True":
        df.to_csv(path_or_buf=new_file_path, sep='\t')
    else:
        df.to_csv(path_or_buf=new_file_path, sep='\t')
    print(f"Cutting {path_to_list(input_file)[-3:]} based on {endpoint}")
    print(f'Rewriting the file as {path_to_list(new_file_path)[-1]}')


parser = argparse.ArgumentParser(description="Cut the files so that we only keep data that we have across all data types.")
parser.add_argument(
    "-c",
    "--cut-files",
    type=str,
    default="False",
    help=("bool on whether to shorten files of a data type so that they only contain the SampleID's"
         " found in the class files."
          )
)
parser.add_argument(
    "-q",
    '--quick',
    type=str,
    default="False",
    help="Shorten files to 3 variables for mini, quick analysis."
)
parser.add_argument(
    "-e",
    '--endpoint',
    type=str,
    default="PFI",
    help="Endpoint that you woul like to use for analysis."
)

args = parser.parse_args()
cut_files = args.cut_files
quick_analysis = args.quick
Analysis_endpoint = args.endpoint

print(f"Cut files set to {cut_files}")
print(f"quick_analysis set to {quick_analysis}")

# get path to input data folders
currentWorkingDir = os.getcwd()
parent_folders = path_to_list(currentWorkingDir)
parent_directory = path_delimiter().join(parent_folders[:-1])
input_data_dir = next(os.walk(os.path.join(*[parent_directory, "InputData"])))[1]

# for unix it would be '{_}' for windows it would be '\'
_=path_delimiter()

map = {} # All of the patients of one cancer type mapped to a path of one data type

for CancerType in sorted(input_data_dir):

    patients_with_all_data_types = set()
    class_info = set()
    patients_per_data_type = []
    cancer_path = os.path.join(*[parent_directory, "InputData", CancerType])
    data_paths = []

    for DataType in sorted(os.listdir(cancer_path), key=lambda s: s.lower()):

        data_type_path = os.path.join(*[parent_directory, "InputData", CancerType, DataType])
        data_paths.append(data_type_path)

        if DataType != "Class":
            for input_file in sorted(os.listdir(data_type_path)):
                # we don't want to re-cut an already cut file
                if is_cut_or_tempfile(input_file):
                    continue

                input_file = f'{data_type_path}{_}{input_file}'
                # In TSV files, patient ID's are the first word of each line
                if input_file.endswith('.tsv'):
                    patients_per_data_type = [line.split('\t')[0] for line in open(input_file)]
                    patients_with_all_data_types = patients_with_all_data_types.intersection(set(patients_per_data_type))
                else:
                    # In TTSV files, patient ID's are the first line
                    with codecs.open(input_file, 'r') as myfile:
                        firstline = myfile.readline()
                        patients_per_data_type = firstline.split('\t')
                        patients_with_all_data_types = patients_with_all_data_types.intersection(set(patients_per_data_type))

        # We expect to open the Class files first since Class comes alphabetically before Clinical, Covariate, CNV, DNA_Methylation, Expression, miRNA, RPPA, and SM
        # This is where we begin to build our set of patients with all_data_types
        else:
            patients_per_data_type = [line.split('\t')[0] for line in open(f'{data_type_path}{_}{Analysis_endpoint}.tsv')]
            patients_with_all_data_types.update(patients_per_data_type)
            class_info.update(patients_per_data_type)

    for DataType in sorted(os.listdir(cancer_path)):
        data_type_path = os.path.join(*[parent_directory, "InputData", CancerType, DataType])
        if cut_files == "True" or quick_analysis == "True":
            run_make_df_function(data_type_path, patients_with_all_data_types, DataType, quick_analysis, Analysis_endpoint)