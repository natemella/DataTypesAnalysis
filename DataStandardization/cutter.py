import os
import pandas as pd
currentWorkingDir = os.path.dirname(os.path.realpath(__file__))
import codecs
from util import *

def filter_cols(input_file, patient_ids):
    df = pd.read_csv(input_file, delimiter='\t',
                       na_values='NA')[patient_ids]
    print(df.columns.values[0:10])
    return df

def filter_rows(input_file, patient_ids, index_name):
    iter_csv = pd.read_csv(input_file, delimiter='\t', iterator=True, chunksize=1000)
    return pd.concat([chunk[chunk[index_name].isin(patient_ids)] for chunk in iter_csv])
def make_df(patient_ids, DataType, input_file):
    print(DataType)

    if input_file.endswith(".ttsv"):
        df = filter_cols(input_file, patient_ids)
    else:
        if DataType != "DNA_methylation":
            index_name = "SampleID"
        else:
            index_name = "Patient_ID"
        df = filter_rows(input_file,patient_ids, index_name)

    print(df.iloc[:3])

my_list = path_to_list(currentWorkingDir)
parent_directory = path_delimiter().join(my_list[:-1])

INPUT_DATA = next(os.walk(os.path.join(*[parent_directory,"InputData"])))[1]

# for unix it would be '{_}' for windows it would be '\'
_=path_delimiter()

sample_summary = open("sample_summary.tsv",'w+')
sample_summary.write("CancerType\tOutcome\tNumber of Patients per type of Data\n")

end_points = ["LT_PFI", "ST_PFI"]

for CancerType in INPUT_DATA:
    for outcome in end_points:
        sample_summary.write(f'{CancerType}\t')
        sample_summary.write(f'{outcome.replace("T_", "")}\t')
        total_patients = set()
        patients_with_all = set()
        class_info = set()
        patients_per_data = []
        for list_of_dTypes in next(os.walk(os.path.join(*[parent_directory,"InputData",CancerType]))):
            already_seen = False
            if len(list_of_dTypes) > 1 and isinstance(list_of_dTypes, list):
                for DataType in list_of_dTypes:
                    d_type_directory = os.path.join(*[parent_directory,"InputData",CancerType,DataType])
                    if DataType != "Class":
                        for input_file in os.listdir(d_type_directory):
                            if already_seen and DataType == "Covariate":
                                continue
                            input_file = f'{d_type_directory}{_}{input_file}'
                            if input_file.endswith(('.tsv','.txt')):
                                patients_per_data = [line.split('\t')[0] for line in open(input_file)]
                                total_patients.update(patients_per_data)
                                patients_with_all = patients_with_all.intersection(set(patients_per_data))
                                sample_summary.write(f'{DataType[0:5]}:{len(patients_with_all)},{len(class_info.intersection(patients_per_data))}')
                            else:
                                with codecs.open(input_file, 'r') as myfile:
                                    firstline = myfile.readline()
                                    patients_per_data = firstline.split('\t')
                                    total_patients.update(patients_per_data)
                                    patients_with_all = patients_with_all.intersection(set(patients_per_data))
                                    sample_summary.write(f'{DataType[0:5]}:{len(patients_with_all)},{len(class_info.intersection(patients_per_data))}')
                            if DataType == "Covariate":
                                already_seen = True
                    else:
                        patients_per_data = [line.split('\t')[0] for line in open(f'{d_type_directory}{_}PFI.txt') if line.strip('\n').split('\t')[1] == outcome]
                        patients_with_all.update(patients_per_data)
                        class_info.update(patients_per_data)
                        sample_summary.write(f'{DataType}:{len(patients_with_all)}')
                    sample_summary.write('\t')
                sample_summary.write('\n')
    sample_summary.write('\n')

sample_summary.close()