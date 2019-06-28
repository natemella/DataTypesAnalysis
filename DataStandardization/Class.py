import os
import pandas as pd
from util import *

current_working_dir = os.path.dirname(os.path.realpath(__file__))
folders = path_to_list(current_working_dir)
parent_directory = os.path.join(*folders[:-1])

def one_cell(row, col):
    return row[col]

def filter_out_middle_range_data(row, df_column_list, lower_cut_off, upper_cut_off):
    event = one_cell(row, df_column_list[0])
    time = one_cell(row, df_column_list[1])
    if (time <= lower_cut_off and event == 1) or time >= upper_cut_off:
        return True
    return False

def convert_time_values_to_classification_labels(row, df_columns_list, upper_cut_off, endpoint):
    time = one_cell(row, df_columns_list[1])
    if time >= upper_cut_off:
        return f'LT_{endpoint}'
    return f'ST_{endpoint}'

end_points = ("DFI", "DSS", "OS", "PFI")

_ = path_delimiter()

for cancer_type in next(os.walk(parent_directory + f"{_}InputData"))[1]:
    for subdir in next(os.walk(parent_directory + f"{_}InputData{_}" + cancer_type)):
        if "Covariate" in subdir:
            covariate_dir = f"{parent_directory}{_}InputData{_}{cancer_type}{_}Covariate"
            for filename in os.listdir(covariate_dir):
                if filename.endswith(".tsv") and not is_temp_file(filename) and not is_cut_file(filename):
                    df = pd.read_csv(filepath_or_buffer=f"{covariate_dir}{_}{filename}", sep="\t", index_col=0)
                    df = df.rename_axis("SampleID")
                    variables = df.columns.values
                    class_df = df[[value for value in variables if value.startswith(end_points)]]
                    Class_dir = f"{parent_directory}{_}InputData{_}{cancer_type}{_}Class{_}"
                    if not os.path.exists(os.path.dirname(Class_dir)):
                        os.makedirs(os.path.dirname(Class_dir))
                    #separate endpoints. Build df of just endpoint + endpoint.time
                    for val in end_points:
                        one_endpoint_df = class_df[[one_endpoint for one_endpoint in variables if one_endpoint.startswith(val)]]
                        average = one_endpoint_df[one_endpoint_df.columns.values[1]].mean()
                        lower_cutoff = average - (180)  # 6 months
                        upper_cutoff = average + (180) # 6 months
                        one_endpoint_df = one_endpoint_df.loc[one_endpoint_df.apply(filter_out_middle_range_data, args=(one_endpoint_df.columns.values, lower_cutoff, upper_cutoff), axis="columns")]
                        final_series = one_endpoint_df.apply(convert_time_values_to_classification_labels, args=(one_endpoint_df.columns.values, upper_cutoff, val), axis="columns")
                        final_series.name = "Class"
                        final_series.to_csv(f"{Class_dir}{val}.tsv", sep="\t", header=True, na_rep="NA")
                    df[[var for var in variables if not var.startswith(end_points)]].to_csv(path_or_buf=f"{covariate_dir}{_}{cancer_type}.tsv", sep="\t", header=True, na_rep='NA')

