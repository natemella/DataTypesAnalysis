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

def drop_non_useful_variables(df):
    with open("Interesting_Clinical_Variables.tsv") as input:
        list_of_variables = input.readline().strip("\n").split('\t')
    columns = df.columns.values
    variables_to_keep = []
    for i in columns:
        if i not in list_of_variables:
            continue
        variables_to_keep.append(i)
    return df[variables_to_keep]

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
    nan_labels = ["[Not Applicable]", "[Not Available]", "[Not Evaluated]", "[Unknown]",
                  "NX", "MX", "TX", "[Discrepancy]", "RX", "GX"]
    one_cancer_df = one_cancer_df.replace(to_replace = nan_labels, value=np.nan)
    one_cancer_df = filter_parse_columns(one_cancer_df)
    one_cancer_df = drop_non_useful_variables(one_cancer_df)
    one_cancer_df = filter_parse_rows(one_cancer_df.T).T
    my_index = one_cancer_df.index.values
    new_index = [patient_id[0:12] for patient_id in my_index]
    one_cancer_df.index = new_index
    one_cancer_df = check_for_duplicates_categorical(one_cancer_df)
    one_cancer_df.to_csv(path_or_buf=('TCGA_' + abbreviations_dict[sample_id] + '.tsv'), sep='\t', na_rep='NA')


