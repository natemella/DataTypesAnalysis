import os
from typing import List


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


def path_delimiter():
    Folders = ['a', 'b']
    x = os.path.join(*Folders)
    return x[1]

def make_relevant_types_list():
    with open("CancerTypes.txt") as file:
        with open("abreviations.tsv") as abr:
            abreviations = [x.strip('\n') for x in file]
            relevant_types = [x.split('\t')[1].strip('\n') for x in abr if x.split('\t')[0] in abreviations]
    return relevant_types

def make_cancer_dict(relevant_types, value_list=[]):
    cancer_dict = {}
    for x in relevant_types:
        cancer_dict[x] = value_list[:]
    return cancer_dict

def make_tss_dict_and_rev_codes_dic(relevant_types):
    relevant_codes = set()
    tss_dictionary = {}
    with open("tss_codes.tsv") as codes:
        codes.readline()
        for x in codes:
            line = x.strip('\n').split('\t')
            if line[2] in relevant_types:
                relevant_codes.add(line[0])
                tss_dictionary[line[0]] = line[2]
    return [relevant_codes, tss_dictionary]

def make_abbrevation_dict(relevant_types):
    abbreviations_dict = {}
    with open("abreviations.tsv") as abr:
        abr.readline()
        for x in abr:
            list = x.strip('\n').split('\t')
            if list[1] in relevant_types:
                abbreviations_dict[list[1]] = list[0]
    return abbreviations_dict

def is_tumor(sample_id):
    if len(sample_id) > 12:
        return sample_id.split("-")[3].startswith("01")
    return True

def fill_cancer_dict(relevant_codes, tss_dictionary, cancer_dict, relevant_types, all_patients, value_list=[]):
    cancer_patient_ids = value_list
    for sample_id in all_patients:
        if sample_id == "sample" or not is_tumor(sample_id):
            continue
        if sample_id.split('-')[1] in relevant_codes:
            cancer_patient_ids.append(sample_id)
            tss = sample_id.split('-')[1]
            for Cancer in relevant_types:
                if tss_dictionary[tss] == Cancer:
                    cancer_dict[Cancer].append(sample_id)
    return cancer_patient_ids

def dictionary_makers(all_patients, value_list=[]):

    relevant_types = make_relevant_types_list()
    cancer_dict = make_cancer_dict(relevant_types, value_list)
    relevant_codes = make_tss_dict_and_rev_codes_dic(relevant_types)[0]
    tss_dictionary = make_tss_dict_and_rev_codes_dic(relevant_types)[1]
    abbreviations_dict = make_abbrevation_dict(relevant_types)
    cancer_patient_ids = fill_cancer_dict(relevant_codes, tss_dictionary, cancer_dict, relevant_types, all_patients, value_list)
    return [relevant_types, relevant_codes, tss_dictionary, abbreviations_dict, cancer_dict, cancer_patient_ids]

def check_for_duplicates(df):
    if True in df.columns.duplicated():
        print("\nFound Duplicates!!!\n")
        print([df.columns.values[i] for i in range(0, len(df.columns.duplicated())) if df.columns.duplicated()[i] == True])
        df = df.groupby(level=0, axis=1).mean()
        return df
    else:
        return df

def get_paths_to_data_files():
    current_working_dir = os.path.dirname(os.path.realpath(__file__))
    my_list = path_to_list(current_working_dir)
    parent_directory = path_delimiter().join(my_list[:-1])
    input_data_folder = next(os.walk(os.path.join(*[parent_directory, "InputData"])))[1]
    list_data_paths: List[str] = []
    _=path_delimiter()
    for CancerType in input_data_folder:
        for list_of_dTypes in next(os.walk(os.path.join(*[parent_directory, "InputData", CancerType]))):
            if len(list_of_dTypes) > 1 and isinstance(list_of_dTypes, list):
                for DataType in list_of_dTypes:
                    d_type_directory = os.path.join(*[parent_directory, "InputData", CancerType, DataType])
                    for input_file in os.listdir(d_type_directory):
                        input_file = f'{d_type_directory}{_}{input_file}'
                        list_data_paths.append(input_file)
    return list_data_paths

def is_cut_or_tempfile(input_file):
    extension = input_file.split('_')[-1]
    if extension.split('.')[0] == "cut" or extension.split('.')[0] == "temp":
        return True
    return False

def is_temp_file(input_file):
    extension = input_file.split('_')
    if extension[-1].split('.')[0] == "temp":
        return True

def is_cut_file(input_file):
    extension = input_file.split('_')
    if extension[-1].split('.')[0] == "cut":
        return True

def get_paths_to_data_type(data_type):
    paths = get_paths_to_data_files()
    return [path for path in paths if path_to_list(path)[-2] == data_type]
