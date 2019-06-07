import pandas as pd
import sys
from util import *

def remove_sparse_rows(df, percent_threshold = 0.2):
    return remove_sparse_columns(df.T, percent_threshold).T

def remove_sparse_columns(df, percent_threshold = 0.2):
    columns_to_keep = []
    column_info_df = df.describe(include='all')
    for column_name in column_info_df.columns.values:
        num_of_existing_values = column_info_df[column_name][0]
        Na_count = len(df.index) - num_of_existing_values
        percent_missing = Na_count / len(df.index)
        if percent_missing < percent_threshold:
            columns_to_keep.append(column_name)
    return df[columns_to_keep]

def truncate_cancer_IDs(df, num_of_char = 12):
    new_index = []
    for ID in df.index.values:
        truncatedID = ID[0:num_of_char]
        new_index.append(truncatedID)
    df.index = new_index
    return df

with open(sys.argv[1]) as input:
    input.readline()
    all_patients = [x.split('\t')[0] for x in input]
    list_of_maps = dictionary_makers(all_patients)


cancer_patient_ids = list_of_maps[5]
cancer_dict = list_of_maps[4]
abbreviations_dict = list_of_maps[3]

df = pd.read_csv("TCGA-RPPA-pancan-clean.xena", sep="\t", index_col="SampleID")
df = df.loc[cancer_patient_ids]
df = df.groupby(['SampleID']).mean()

nrow, ncol = df.shape

df = remove_sparse_columns(df)
df = remove_sparse_rows(df)
df = df.rename_axis("SampleID")

nrow_post, ncol_post = df.shape

print(f"Proteins removed = {ncol - ncol_post}")
print(f'Tumors removed = {nrow - nrow_post}')

for cancer in cancer_dict:
    one_cancer_df = df.loc[cancer_dict[cancer]]
    one_cancer_df = truncate_cancer_IDs(one_cancer_df)
    one_cancer_df.to_csv(path_or_buf=('TCGA_' + abbreviations_dict[cancer] + '.tsv'), sep='\t', na_rep='NA')