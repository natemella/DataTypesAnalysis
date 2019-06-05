import pandas as pd
import numpy as np
from util import *

with open("Clinical_Variables.csv") as data:
    variable_list = data.readline().strip('\n').split(',')

input = pd.read_excel("mmc1.xlsx", index_col="bcr_patient_barcode")
header = input.columns.values
all_patients = input.index

list_of_dictionaries = dictionary_makers(all_patients)

# [relevant_types, relevant_codes, tss_dictionary, abbreviations_dict, cancer_dict, cancer_patient_ids]

relevant_types = list_of_dictionaries[0]
relevant_codes = list_of_dictionaries[1]
tss_dictionary = list_of_dictionaries[2]
abbreviations_dict = list_of_dictionaries[3]
cancer_dict = list_of_dictionaries[4]
cancer_patient_ids = list_of_dictionaries[5]

df = pd.read_excel("mmc1.xlsx", sep="\t", index_col="bcr_patient_barcode")
df = df.drop(labels="Unnamed: 0", axis=1)

df = df.loc[cancer_patient_ids]

endpoints = ("DFI","DSS","OS","PFI")

for sample_id in cancer_dict:
    one_cancer_df = df.loc[cancer_dict[sample_id]]
    one_cancer_df = one_cancer_df.replace("[Not Applicable]", np.nan).replace("[Not Available]", np.nan)
    df_info = one_cancer_df.describe(include="all")
    columns = df_info.columns.values
    variables_to_keep = []
    variables_to_drop = []
    for i in columns:
        if i not in variable_list:
            variables_to_drop.append(i)
            continue

        if i.startswith(endpoints):
            variables_to_keep.append(i)
            continue

        Na_count = len(one_cancer_df.index) - df_info[i][0]
        percent_missing = Na_count / len(one_cancer_df.index)
        if percent_missing > 0.2:
            variables_to_drop.append(i)
        else:
            variables_to_keep.append(i)

    one_cancer_df = one_cancer_df[variables_to_keep]
    one_cancer_df.to_csv(path_or_buf=('TCGA_' + abbreviations_dict[sample_id] + '.tsv'), sep='\t', na_rep='NA')
