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
    print(f'Finished Step 2.{step}')
    step+=1
    if True in df.columns.duplicated():
        df = df.astype(float)
        print("\nFound Duplicates!!!\n")
        print([df.columns.values[i] for i in range(0, len(df.columns.duplicated())) if df.columns.duplicated()[i] == True])
        df = df.groupby(level=0, axis=1).mean()

    new_columns = []
    #truncate the IDs to twelve characters
    for ID in df.columns.values:
        truncatedID = ID[0:12]
        new_columns.append(truncatedID)

    df.columns = new_columns
    print(f'Beginning to write DataFrame to file')
    df.to_csv(path_or_buf=('TCGA_' + abbreviations_dict[x] + '.ttsv'), sep='\t', na_rep="NA", index=False)
    print(f'Finished Evaluating TCGA_{abbreviations_dict[x]}')