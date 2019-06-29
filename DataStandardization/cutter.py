import os
import pandas as pd
currentWorkingDir = os.path.dirname(os.path.realpath(__file__))
import codecs
from util import *
import argparse

def run_make_df_function(d_type_directory, patients_with_all, DataType, quick_analysis, endpoint):
        if DataType == "Class":
            return
        for input_file in os.listdir(d_type_directory):
            if is_cut_or_tempfile(input_file):
                continue
            input_file = f'{d_type_directory}{_}{input_file}'
            make_df(patients_with_all, DataType, input_file, quick_analysis, endpoint)

def filter_cols(input_file, patient_ids, mini):
    my_cols = list(patient_ids)
    my_cols.insert(0,"SampleID")
    df = pd.read_csv(input_file, delimiter='\t',
                       na_values='NA', usecols=my_cols, index_col="SampleID")
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
    print(f"Cutting {path_to_list(input_file)[-1]} and making a new copy based on all patients "
          f"who have data for across all data types and {endpoint} data")



parser = argparse.ArgumentParser(description="Develop a summary of file information and cut the file.")
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
if quick_analysis == "True":
    cut_files = "True"

my_list = path_to_list(currentWorkingDir)
parent_directory = path_delimiter().join(my_list[:-1])

input_data_dir = next(os.walk(os.path.join(*[parent_directory, "InputData"])))[1]

# for unix it would be '{_}' for windows it would be '\'
_=path_delimiter()

sample_summary = open("sample_summary.csv",'w+')
sample_summary.write("CancerType,Outcome,Class Info,Number of Patients per type of Data,Patients with all 7 data types\n")

end_points = [f"LT_{Analysis_endpoint}", f"ST_{Analysis_endpoint}"]
vital_map = {}
for CancerType in input_data_dir:
    print(CancerType)
    for outcome in end_points:
        sample_summary.write(f'{CancerType},')
        sample_summary.write(f'{outcome.replace("T_", "")},')
        total_patients = set()
        patients_with_all = set()
        class_info = set()
        patients_per_data = []
        for list_of_dTypes in next(os.walk(os.path.join(*[parent_directory,"InputData",CancerType]))):
            list_of_paths = []
            already_seen = False
            if len(list_of_dTypes) > 1 and isinstance(list_of_dTypes, list):
                for DataType in list_of_dTypes:
                    d_type_directory = os.path.join(*[parent_directory,"InputData",CancerType,DataType])
                    list_of_paths.append(d_type_directory)
                    if DataType != "Class":
                        for input_file in os.listdir(d_type_directory):
                            if is_cut_or_tempfile(input_file):
                                continue
                            input_file = f'{d_type_directory}{_}{input_file}'
                            if input_file.endswith(('.tsv','.txt')):
                                patients_per_data = [line.split('\t')[0] for line in open(input_file)]
                                total_patients.update(patients_per_data)
                                patients_with_all = patients_with_all.intersection(set(patients_per_data))
                                sample_summary.write(f'{DataType[0:5]}:Total={len(patients_per_data)} & {Analysis_endpoint}={len(class_info.intersection(patients_per_data))}')
                            else:
                                with codecs.open(input_file, 'r') as myfile:
                                    firstline = myfile.readline()
                                    patients_per_data = firstline.split('\t')
                                    total_patients.update(patients_per_data)
                                    patients_with_all = patients_with_all.intersection(set(patients_per_data))
                                    sample_summary.write(f'{DataType[0:5]}:Total={len(patients_per_data)} & {Analysis_endpoint}={len(class_info.intersection(patients_per_data))}')

                    else:
                        patients_per_data = [line.split('\t')[0] for line in open(f'{d_type_directory}{_}{Analysis_endpoint}.tsv') if line.strip('\n').split('\t')[1] == outcome]
                        patients_with_all.update(patients_per_data)
                        class_info.update(patients_per_data)
                        sample_summary.write(f'{DataType}:{len(patients_with_all)},')
                    sample_summary.write(' | ')
                sample_summary.write(f',{len(patients_with_all)}\n')
                for path in list_of_paths:
                    if outcome == f"LT_{Analysis_endpoint}":
                        vital_map[path] = patients_with_all
                    else:
                        vital_map[path].update(patients_with_all)
    sample_summary.write('\n')

sample_summary.close()

for CancerType in input_data_dir:
    for list_of_dTypes in next(os.walk(os.path.join(*[parent_directory,"InputData",CancerType]))):
        if len(list_of_dTypes) > 1 and isinstance(list_of_dTypes, list):
            for DataType in list_of_dTypes:
                d_type_directory = os.path.join(*[parent_directory,"InputData",CancerType,DataType])
                patients_with_all = vital_map[d_type_directory]
                if cut_files == "True":
                    print(DataType)
                    run_make_df_function(d_type_directory, patients_with_all, DataType, quick_analysis, Analysis_endpoint)