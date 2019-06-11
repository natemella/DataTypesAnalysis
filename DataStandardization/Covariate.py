import pandas as pd
import numpy as np
import argparse
from util import *

def filter_parse_columns(one_cancer_df):
    end_points = ("PFI", "OS", "DSS", "DFI")
    df_describe = one_cancer_df.describe(include="all")
    columns = df_describe.columns.values
    variables_to_keep = []
    variables_to_drop = []
    for i in columns:
        if i not in variable_list:
            variables_to_drop.append(i)
            continue
        if i.startswith(end_points):
            variables_to_keep.append(i)
            continue
        if i == "DFI":
            print("FREAK")
        Na_count = len(one_cancer_df.index) - df_describe[i][0]
        percent_missing = Na_count / len(one_cancer_df.index)
        if percent_missing > 0.2:
            variables_to_drop.append(i)
        else:
            variables_to_keep.append(i)
    return one_cancer_df[variables_to_keep]

def one_cell(row, col):
    return row[col]

def filter_out_middle_range_data(row, df_column_list, lower_cut_off, upper_cut_off):
    event = one_cell(row, df_column_list[0])
    time = one_cell(row, df_column_list[1])
    if (time <= lower_cut_off and event == 1) or time >= upper_cut_off:
        return True
    return False

def index_after_class_filter(df, endpoint):
    variables = df.columns.values
    class_df = df[[value for value in variables if value.startswith(endpoint)]]
    # separate endpoints. Build df of just endpoint + endpoint.time
    one_endpoint_df = class_df[[one_endpoint for one_endpoint in variables if one_endpoint.startswith(endpoint)]]
    average = one_endpoint_df[one_endpoint_df.columns.values[1]].mean()
    lower_cutoff = average - (180)  # 6 months
    upper_cutoff = average + (180)  # 6 months
    one_endpoint_df = one_endpoint_df.loc[one_endpoint_df.apply(filter_out_middle_range_data, args=(
        one_endpoint_df.columns.values, lower_cutoff, upper_cutoff), axis="columns")]
    return one_cancer_df.index.values

def filter_parse_row(df, endpoint):
    df = df[np.isfinite(df[f'{endpoint}.time'])]
    new_index = index_after_class_filter(df, endpoint)
    return df[df.index.isin(new_index)]

parser = argparse.ArgumentParser(description="Decide which endpoint to keep.")
parser.add_argument(
    "file-name",
    type=str,
    help="Name of excell file with Covariate Data"

)
parser.add_argument(
    "-e",
    "--endpoint",
    type=str,
    default="PFI",
    help="Potential endpoints are PFI, OS, DSS, DFI."

)
args = parser.parse_args()
end_point = args.endpoint
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


for sample_id in cancer_dict:
    one_cancer_df = df.loc[cancer_dict[sample_id]]
    one_cancer_df = one_cancer_df.replace("[Not Applicable]", np.nan).replace("[Not Available]", np.nan)
    one_cancer_df = one_cancer_df.replace("[Not Evaluated]", np.nan).replace("[Unknown]", np.nan)
    one_cancer_df = filter_parse_row(one_cancer_df,end_point)
    one_cancer_df = filter_parse_columns(one_cancer_df)
    one_cancer_df.to_csv(path_or_buf=('TCGA_' + abbreviations_dict[sample_id] + '.tsv'), sep='\t', na_rep='NA')
