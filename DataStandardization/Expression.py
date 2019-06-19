import pandas as pd
import sys
from util import *

with open(sys.argv[1]) as input:
    all_patients= [x for x in input.readline().strip('\n').split('\t') if x != '']
    list_of_dictionaries = dictionary_makers(all_patients)
    index_col = [line.split('\t')[0] for line in input]

abbreviations_dict = list_of_dictionaries[3]
cancer_dict = list_of_dictionaries[4]
print("Finished Step 1")

step = 1
for x in cancer_dict:
    df = pd.read_csv(sys.argv[1], delimiter='\t', usecols=cancer_dict[x], engine='c', na_values='NA')[cancer_dict[x]].astype(float)
    series = pd.Series(index_col)
    series.name = "SampleID"
    df = pd.concat([series, df], axis=1)
    step += 1

    new_columns = []
    #truncate the IDs to twelve characters
    for ID in df.columns.values:
        truncatedID = ID[0:12]
        new_columns.append(truncatedID)

    df.columns = new_columns
    df = df.set_index("SampleID")
    df = check_for_duplicates(df)

    print(f'Beginning to write {abbreviations_dict[x]} DataFrame to file')
    df.to_csv(path_or_buf=('TCGA_' + abbreviations_dict[x] + '.ttsv'), sep='\t', na_rep="NA")
    print(f'Finished Evaluating TCGA_{abbreviations_dict[x]}')