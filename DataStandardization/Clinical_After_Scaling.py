import pandas as pd
import roman
import os
from util import *

def fix_neoplasm_histologic_grade(df):
    new_col = []
    for value in df.neoplasm_histologic_grade:
        if pd.isna(value):
            new_col.append(value)
        elif value == "High Grade":
            new_col.append(3)
        else:
            new_col.append(int(value[1]))
    df.neoplasm_histologic_grade = new_col
    return df

def convert_stage_to_integer(df, variable):
    df[variable] = [int(data_point[1]) if not pd.isna(data_point) else data_point for data_point in df[variable]]
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
    for i in categorical_columns:
        if len(categorical_columns[i]) == 1:
            variables_to_drop.append(i)
    return df[[item for item in df.columns.values if item not in variables_to_drop]]

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

def split_and_one_hot_encode(series, name):
    unique_values = set()
    for x in series:
        if isinstance(x, float):
            continue
        x = x.split("|")
        unique_values.update(x)
    return build_data_frame(series, unique_values, name)

def filter_anatomic_neoplasm_subdivision(df):
    column = df["anatomic_neoplasm_subdivision"]
    new_df= split_and_one_hot_encode(column, "anatomic_neoplasm_subdivision")
    df = df.drop("anatomic_neoplasm_subdivision", axis="columns")
    df = pd.concat([df, new_df], axis=1)
    return df

def filter_history_thyroid_disease(df):
    column = df.history_thyroid_disease
    new_df= split_and_one_hot_encode(column, "history_thyroid_disease")
    df = df.drop("history_thyroid_disease", axis="columns")
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
    new_df.index = df.index
    df = df.drop("laterality", axis="columns")
    df = pd.concat([df, new_df], axis=1)
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

def convert_hemoglobin_or_palate_to_numbers(df, category):
    new_col= []
    for data in df[category]:
        if data == "Low":
            new_col.append(0)
        elif data == "Normal":
            new_col.append(1)
        elif data == "Elevated":
            new_col.append(2)
        else:
            new_col.append(data)
    df[category] = new_col
    return df


if os.path.exists("excluded_categories.txt"):
    os.remove("excluded_categories.txt")

stage_variables= ["clinical_N", "clinical_M", "clinical_T", "ajcc_nodes_pathologic_pn",
                  "residual_tumor", "tumor_grade", "pathologic_T"]

current_working_dir = os.path.dirname(os.path.realpath(__file__))
my_list = path_to_list(current_working_dir)
parent_directory = path_delimiter().join(my_list[:-1])
input_data_folder = os.path.join(*[parent_directory, "InputData"])
list_of_paths = [x for x in get_paths_to_data_files() if path_to_list(x)[-2] == "Clinical"]

for file in list_of_paths:
    f = path_to_list(file)[-1]
    print(f)

    if f.startswith("TCGA"):
        cancer = f.replace(".tsv","").replace("TCGA_","")
        one_cancer_df = pd.read_csv(file, sep="\t", low_memory=False, index_col=0)
        print(cancer)
        for variable in stage_variables:
            if variable in one_cancer_df.columns.values:
                one_cancer_df = convert_stage_to_integer(one_cancer_df, variable)

        if "history_other_malignancy" in one_cancer_df.columns.values:
            one_cancer_df = combine_yes_values_history_other_malignancy(one_cancer_df)
        if "race" in one_cancer_df.columns.values:
            one_cancer_df = adjust_race_labels(one_cancer_df)
        if "anatomic_neoplasm_subdivision" in one_cancer_df.columns.values:
            one_cancer_df = filter_anatomic_neoplasm_subdivision(one_cancer_df)
        if "history_thyroid_disease" in one_cancer_df.columns.values:
            one_cancer_df = filter_history_thyroid_disease(one_cancer_df)
        if "ajcc_tumor_pathologic_pt" in one_cancer_df.columns.values:
            one_cancer_df = fix_ajcc_tumor_pathologic_pt_labels(one_cancer_df)
        if "ajcc_pathologic_tumor_stage" in one_cancer_df.columns.values:
            one_cancer_df = fix_tumor_stage_labels(one_cancer_df, cancer)
        if "clinical_stage" in one_cancer_df.columns.values:
            one_cancer_df = fix_clinical_stage_labels(one_cancer_df)

        if "extrathyroidal_extension" in one_cancer_df.columns.values:
            one_cancer_df =filter_extrathyroidal_extension(one_cancer_df)

        if cancer == "BLCA":
            one_cancer_df = one_cancer_df.drop(["history_neoadjuvant_treatment", "ethnicity"], axis="columns")

        if cancer == "LGG":
            one_cancer_df = one_cancer_df.drop(["history_neoadjuvant_treatment", "history_ionizing_rt_to_head"], axis="columns")
            one_cancer_df = combine_small_categories(one_cancer_df, "tumor_site")

        if cancer == "HNSC":
            one_cancer_df = one_cancer_df.drop(["histologic_diagnosis", "alcohol_history_documented"], axis="columns")
            one_cancer_df = combine_small_categories(one_cancer_df, "anatomic_organ_subdivision")

        if cancer == "HNSC" or "LUAD":
            if "tobacco_smoking_history_indicator" in one_cancer_df.columns.values:
                one_cancer_df = combine_smoking_history(one_cancer_df)

        if cancer == "KIRC":
            one_cancer_df = change_laterality_to_binary(one_cancer_df)
            one_cancer_df = convert_hemoglobin_or_palate_to_numbers(one_cancer_df, "hemoglobin_level")
            one_cancer_df = convert_hemoglobin_or_palate_to_numbers(one_cancer_df, "platelet_count")

        if cancer == "LUAD":
            one_cancer_df = one_cancer_df.drop("history_neoadjuvant_treatment", axis="columns")
            one_cancer_df = combine_anatomic_subdivision(one_cancer_df)
            one_cancer_df = combine_small_categories(one_cancer_df, "histologic_diagnosis.1")

        if cancer == "UCEC":
            one_cancer_df = one_cancer_df.drop("history_neoadjuvant_treatment", axis="columns")
            one_cancer_df = fix_neoplasm_histologic_grade(one_cancer_df)

        one_cancer_df = check_num_of_patients_per_category(one_cancer_df)
        one_cancer_df = one_cancer_df.rename_axis("SampleID")
        one_cancer_df.to_csv(path_or_buf=file, sep='\t', na_rep='NA')