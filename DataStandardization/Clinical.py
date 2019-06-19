import pandas as pd
import numpy as np
import sys
import os
from util import *

def check_for_duplicates_categorical(df):
    if True in df.index.duplicated():
        print("\nFound Duplicates!!!\n")
        print([df.index.values[i] for i in range(0, len(df.index.duplicated())) if df.index.duplicated()[i] == True])
        df = df.loc[~df.index.duplicated(keep="first")]
        return df
    else:
        return df

def letter_to_number(mystring):
    new_string = ""
    for c in mystring:
        if c.isalpha():
            new_string += str(ord(c) -96)
        else:
            new_string += str(c)
    return float(new_string)

def filter_ajcc_tumor_pathologic_pt(row):
    value = row["ajcc_tumor_pathologic_pt"]
    if isinstance(value, float):
        return
    else:
        value = value.replace("T","0.")
    return letter_to_number(value)

def fix_ajcc_tumor_pathologic_pt_labels(df):
    series = df.apply(filter_ajcc_tumor_pathologic_pt, axis="columns")
    series.name = "ajcc_tumor_pathologic_pt"
    df = df.drop("ajcc_tumor_pathologic_pt", axis=1)
    df = pd.concat([df,series], axis=1)
    return df

def is_categorical(df, col_name):
    for item in df[col_name].values:
        if isinstance(item, str):
            return True
    return False

def build_data_frame(series, unique_values, name):
    columns = [f'{name}_{value}' for value in unique_values]
    my_map = {}
    for col_name in columns:
        my_map[col_name] = []
        for value in series.values:
            if isinstance(value, float):
                my_map[col_name].append(0)
                continue
            value = value.split("|")
            if col_name.replace(f'{name}_',"") in value:
                my_map[col_name].append(1)
            else:
                my_map[col_name].append(0)
    df = pd.DataFrame(my_map)
    df.index = series.index
    return df

def check_num_of_patients_per_category(df):
    categorical_columns = {}
    for i in df.columns.values:
        if is_categorical(df, i):
            groups = set(df[i].values)
            if len(groups) > 50:
                continue
            categorical_columns[i] = []
            my_map = {}
            for group in groups:
                if pd.isna(group):
                    continue
                my_map[group] = len([x for x in df[i].values if x == group])
            for x in my_map:
                categorical_columns[i].append(f'{x}:{my_map[x]}')

    df = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in categorical_columns.items() ]))
    df.to_csv(path_or_buf=("category_info.tsv"), sep='\t')



def find_all_unique_values(series, name):
    unique_values = set()
    for x in series:
        if isinstance(x, float):
            continue
        x = x.split("|")
        unique_values.update(x)
    return build_data_frame(series, unique_values, name)

def filter_anatomic_neoplasm_subdivision(df):
    column = df["anatomic_neoplasm_subdivision"]
    new_df= find_all_unique_values(column, "anatomic_neoplasm_subdivision")
    df = df.drop("anatomic_neoplasm_subdivision", axis=1)
    df = pd.concat([df, new_df], axis=1)
    return df

def filter_parse_rows(one_cancer_df):
    df_describe = one_cancer_df.describe(include="all")
    columns = df_describe.columns.values
    variables_to_keep = []
    variables_to_drop = []
    for i in columns:
        Na_count = len(one_cancer_df.index) - df_describe[i][0]
        percent_missing = Na_count / len(one_cancer_df.index)
        if percent_missing > 0.2:
            variables_to_drop.append(i)
        else:
            variables_to_keep.append(i)
    return one_cancer_df[variables_to_keep]

def filter_parse_columns(df):
    return filter_parse_rows(df.T)

with open(sys.argv[1]) as input:
    all_patients = input.readline().strip('\n').split('\t')

all_patients = [patient for patient in all_patients if patient[13:15] == "01"]


list_of_dictionaries = dictionary_makers(all_patients)
relevant_types = list_of_dictionaries[0]
relevant_codes = list_of_dictionaries[1]
tss_dictionary = list_of_dictionaries[2]
abbreviations_dict = list_of_dictionaries[3]
cancer_dict = list_of_dictionaries[4]
cancer_patient_ids = list_of_dictionaries[5]

full_df = pd.read_csv(sys.argv[1], sep="\t", low_memory=False, index_col=0)
full_df = full_df[cancer_patient_ids]


for sample_id in cancer_dict:
    one_cancer_df = full_df[cancer_dict[sample_id]]
    one_cancer_df = one_cancer_df.replace("[Not Applicable]", np.nan).replace("[Not Available]", np.nan)
    one_cancer_df = one_cancer_df.replace("[Not Evaluated]", np.nan).replace("[Unknown]", np.nan)
    one_cancer_df = filter_parse_columns(one_cancer_df)
    one_cancer_df = filter_parse_rows(one_cancer_df.T).T
    my_index = one_cancer_df.index.values
    new_index = [patient_id[0:12] for patient_id in my_index]
    one_cancer_df.index = new_index

    if abbreviations_dict[sample_id] == "BLCA":
        one_cancer_df = check_for_duplicates_categorical(one_cancer_df)
        one_cancer_df = filter_anatomic_neoplasm_subdivision(one_cancer_df)
        one_cancer_df = fix_ajcc_tumor_pathologic_pt_labels(one_cancer_df)
        one_cancer_df.to_csv(path_or_buf=('TCGA_' + abbreviations_dict[sample_id] + '.tsv'), sep='\t', na_rep='NA')
        check_num_of_patients_per_category(one_cancer_df)

