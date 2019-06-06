import pandas as pd
import sys
from util import *

with open(sys.argv[1]) as input:
    all_patients= input.readline().strip('\n').split('\t')
    list_of_dicts = dictionary_makers(all_patients, value_list=['sample'])
    abbreviations_dict = list_of_dicts[3]
    CancerDict = list_of_dicts[4]
print("Finished Step 1")

step = 1
for x in CancerDict:
    df = pd.read_csv(sys.argv[1], delimiter='\t', usecols=CancerDict[x], engine='c', na_values='NA')[CancerDict[x]]
    df = df.set_index("sample")
    df = df.rename_axis("SampleID")
    print(f'Finished Step 2.{step}')
    step += 1
    if True in df.columns.duplicated():
        df = df.astype(float)
        print("\nFound Duplicates!!!\n")
        df = df.groupby(level=0, axis=1).mean()

    new_columns = []
    for ID in df.columns.values:
        truncatedID = ID[0:12]
        new_columns.append(truncatedID)

    df.columns = new_columns
    print(f'Beginning to write {abbreviations_dict[x]} DataFrame to file')
    df.to_csv(path_or_buf=('TCGA_' + abbreviations_dict[x] + '.ttsv'), sep='\t', na_rep="NA")
    print(f'Finished Evaluating TCGA_{abbreviations_dict[x]}')