import pandas as pd
import numpy as np
import sys
import roman
import os
from util import *

def fix_nodes_labels(df):
    df.ajcc_nodes_pathologic_pn = [int(data_point[1]) if not pd.isna(data_point) else data_point for data_point in df.ajcc_nodes_pathologic_pn]
    return df

def fix_clinical_T_lables(df):
    df.clinical_T = [int(data_point[1]) if not pd.isna(data_point) else data_point for data_point in df.clinical_T]
    return df

def fix_clinical_N_lables(df):
    df.clinical_N = [int(data_point[1]) if not pd.isna(data_point) else data_point for data_point in df.clinical_N]
    return df

def fix_clinical_M_lables(df):
    df.clinical_M = [int(data_point[1]) if not pd.isna(data_point) else data_point for data_point in df.clinical_M]
    return df

def fix_residual_tumor(df):
    df.residual_tumor = [int(data_point[1]) if not pd.isna(data_point) else data_point for data_point in df.residual_tumor]
    return df

def fix_tumor_grade(df):
    df.tumor_grade = [int(data_point[1]) if not pd.isna(data_point) else data_point for data_point in df.tumor_grade]
    return df

def adjust_race_labels(df):
    df.race = ["OTHER" if data in ["ASIAN","NATIVE HAWAIIAN OR OTHER PACIFIC ISLANDER","AMERICAN INDIAN OR ALASKA NATIVE"] else data for data in df.race]
    return df

def combine_yes_values_history_other_malignancy(df):
    df.history_other_malignancy = ["Yes" if not pd.isna(data_point) and "Yes" in data_point else data_point for data_point in df.history_other_malignancy]
    return df

def fix_tumor_stage_labels(df, cancer_type):
    series = df.ajcc_pathologic_tumor_stage
    new_column = []
    for data_point in series.values:
        if pd.isna(data_point):
            new_column.append(data_point)
            continue
        data_point = data_point.replace("Stage ",'')
        if data_point in ["Tis", "N0", "M0"]:
            new_column.append(0)
            continue
        for character in data_point:
            if character in ["A", "B", "C"]:
                data_point = data_point.replace(character, "")
        new_column.append(roman.fromRoman(data_point))
    # merge stage 1 into stage 2 for BLCA because there aren't enough stage 1 patients
    if cancer_type == "BLCA":
        new_column = [2.0 if x == 1.0 else x for x in new_column]

    df.ajcc_pathologic_tumor_stage = new_column
    return df

def fix_clinical_stage_labels(df):
    series = df.clinical_stage
    new_column = []
    for data_point in series.values:
        if pd.isna(data_point):
            new_column.append(data_point)
            continue
        data_point = data_point.replace("Stage ", '')
        if data_point in ["Tis", "N0", "M0"]:
            new_column.append(0)
            continue
        for character in data_point:
            if character in ["A", "B", "C"] or character.isdigit():
                data_point = data_point.replace(character, "")
        new_column.append(roman.fromRoman(data_point))
    df.clinical_stage = new_column
    return df


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
    if pd.isna(value):
        return value
    else:
       return int(value[1])

def fix_ajcc_tumor_pathologic_pt_labels(df):
    series = df.apply(filter_ajcc_tumor_pathologic_pt, axis="columns")
    series.name = "ajcc_tumor_pathologic_pt"
    df.ajcc_tumor_pathologic_pt = series
    return df

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def is_categorical(df, col_name):
    for item in df[col_name].values:
        if is_number(item):
            return False
        if isinstance(item, str):
            return True
    print(df[col_name].values)
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
    variables_to_drop = []
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
    with open("excluded_categories.txt", 'a') as out:
        for i in categorical_columns:
            if len(categorical_columns[i]) == 1:
                variables_to_drop.append(i)
                print(f'\n{i}')
                out.write(f'\n{i}\n')
                print(f'{categorical_columns[i]}\n')
                out.write(f'{categorical_columns[i]}\n\n')
                continue
            for item in categorical_columns[i]:
                item = item.split(":")
                if int(item[-1]) < 5:
                    print(f'\n{i}')
                    out.write(f'\n{i}\n')
                    print(f'{categorical_columns[i]}\n')
                    out.write(f'{categorical_columns[i]}\n\n')
                    break
                # variables_to_drop.append(i)
    return df[[item for item in df.columns.values if item not in variables_to_drop]]
    # df = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in categorical_columns.items() ]))
    # df.to_csv(path_or_buf=("category_info.tsv"), sep='\t')

def filter_extrathyroidal_extension(df):
    adjusted_data = []
    for value in df.extrathyroidal_extension:
        if value == "None":
            adjusted_data.append(0)
        elif value == "Minimal (T3)":
            adjusted_data.append(3)
        elif value == "Moderate/Advanced (T4a)" or "Very Advanced (T4b)":
            adjusted_data.append(4)
        else:
            adjusted_data.append(value)
    df.extrathyroidal_extension = adjusted_data
    return df

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

def filter_history_thyroid_disease(df):
    column = df.history_thyroid_disease
    new_df= find_all_unique_values(column, "history_thyroid_disease")
    df = df.drop("history_thyroid_disease", axis=1)
    df = pd.concat([df, new_df], axis=1)
    return df


def combine_small_categories(df, variable):
    my_set = set(df[variable])
    my_map = {}
    for category in my_set:
        my_map[category] = len([data for data in df[variable] if data == category])
    df[variable] = ["Other" if my_map[data_point] < 10 else data_point for data_point in df[variable]]
    return df

def combine_smoking_history(df):
    df.tobacco_smoking_history_indicator = ["Current reformed smoker for < or = 15 years" if data == "Current Reformed Smoker, Duration Not Specified" else data for data in df.tobacco_smoking_history_indicator]
    return df

def change_laterality_to_binary(df):
    right_side = [1 if data == "Right" or data == "Bilateral" else 0 for data in df.laterality]
    left_side = [1 if data == "Left" or data == "Bilateral" else 0 for data in df.laterality]
    new_df = pd.DataFrame({'laterality_right':right_side,'laterality_left':left_side})
    df = df.drop("laterality", axis=1)
    df = pd.concat([df,new_df],axis=1)
    return df

def combine_anatomic_subdivision(df):
    new_col = []
    for data in df.anatomic_organ_subdivision:
        if data == "Other (please specify)" or data == "Bronchial":
            new_col.append("Other")
        else:
            new_col.append(data)
    df.anatomic_organ_subdivision = new_col
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

if os.path.exists("excluded_categories.txt"):
    os.remove("excluded_categories.txt")

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
    with open("excluded_categories.txt", 'a') as out:
        out.write(f"###############################\n"
                  f"BEGINNING TO WRITE TCGA_{abbreviations_dict[sample_id]}\n"
                  f"###############################\n")
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

    if "race" in one_cancer_df.columns.values:
        one_cancer_df = adjust_race_labels(one_cancer_df)
    if "tumor_grade" in one_cancer_df.columns.values:
        one_cancer_df = fix_tumor_grade(one_cancer_df)
    if "residual_tumor" in one_cancer_df.columns.values:
        one_cancer_df = fix_residual_tumor(one_cancer_df)
    if "ajcc_nodes_pathologic_pn" in one_cancer_df.columns.values:
        one_cancer_df = fix_nodes_labels(one_cancer_df)
    if "anatomic_neoplasm_subdivision" in one_cancer_df.columns.values:
        one_cancer_df = filter_anatomic_neoplasm_subdivision(one_cancer_df)
    if "history_thyroid_disease" in one_cancer_df.columns.values:
        one_cancer_df = filter_history_thyroid_disease(one_cancer_df)
    if "ajcc_tumor_pathologic_pt" in one_cancer_df.columns.values:
        one_cancer_df = fix_ajcc_tumor_pathologic_pt_labels(one_cancer_df)
    if "ajcc_pathologic_tumor_stage" in one_cancer_df.columns.values:
        one_cancer_df = fix_tumor_stage_labels(one_cancer_df, abbreviations_dict[sample_id])
    if "clinical_stage" in one_cancer_df.columns.values:
        one_cancer_df = fix_clinical_stage_labels(one_cancer_df)

    if "clinical_T" in one_cancer_df.columns.values:
        one_cancer_df = fix_clinical_T_lables(one_cancer_df)
    if "clinical_M" in one_cancer_df.columns.values:
        one_cancer_df = fix_clinical_M_lables(one_cancer_df)
    if "clinical_N" in one_cancer_df.columns.values:
        one_cancer_df = fix_clinical_N_lables(one_cancer_df)
    if "extrathyroidal_extension" in one_cancer_df.columns.values:
        one_cancer_df =filter_extrathyroidal_extension(one_cancer_df)

    if abbreviations_dict[sample_id] == "BLCA":
        one_cancer_df = one_cancer_df.drop(["history_neoadjuvant_treatment","ethnicity"], axis="columns")
    if abbreviations_dict[sample_id] in ["LGG","KIRC","PRAD"]:
        one_cancer_df = combine_yes_values_history_other_malignancy(one_cancer_df)
    if abbreviations_dict[sample_id] == "LGG":
        one_cancer_df = one_cancer_df.drop(["history_neoadjuvant_treatment","history_ionizing_rt_to_head"], axis="columns")
        one_cancer_df = combine_small_categories(one_cancer_df, "tumor_site")
    if abbreviations_dict[sample_id] == "HNSC":
        one_cancer_df = one_cancer_df.drop("histologic_diagnosis", axis="columns")
        one_cancer_df = combine_small_categories(one_cancer_df, "anatomic_organ_subdivision")
    if abbreviations_dict[sample_id] == "HNSC" or "LUAD":
        if "tobacco_smoking_history_indicator" in one_cancer_df.columns.values:
            one_cancer_df = combine_smoking_history(one_cancer_df)
    if abbreviations_dict[sample_id] == "KIRC":
        one_cancer_df = change_laterality_to_binary(one_cancer_df)
    if abbreviations_dict[sample_id] == "LUAD":
        one_cancer_df = one_cancer_df.drop("history_neoadjuvant_treatment", axis=1)
        one_cancer_df = combine_anatomic_subdivision(one_cancer_df)
        one_cancer_df = combine_small_categories(one_cancer_df, "histologic_diagnosis.1")
    if abbreviations_dict[sample_id] == "UCEC":
        one_cancer_df = one_cancer_df.drop("history_neoadjuvant_treatment", axis=1)

    one_cancer_df = check_num_of_patients_per_category(one_cancer_df)
    one_cancer_df.to_csv(path_or_buf=('TCGA_' + abbreviations_dict[sample_id] + '.tsv'), sep='\t', na_rep='NA')


