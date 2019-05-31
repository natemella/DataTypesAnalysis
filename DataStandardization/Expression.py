import pandas as pd
import sys

with open("CancerTypes.txt") as file:
    with open("abreviations.tsv") as abr:
        abreviations = [x.strip('\n') for x in file]
        RelevantTypes = [x.split('\t')[1].strip('\n') for x in abr if x.split('\t')[0] in abreviations]

CancerDict = {}
for x in RelevantTypes:
    CancerDict[x] = []

TSSDictionary = {}

RelevantCodes = set()

#include the index column in each list



with open("TSS_CODES.tsv") as codes:
    first_line = codes.readline()
    for x in codes:
        line = x.strip('\n').split('\t')
        if line[2] in RelevantTypes:
            RelevantCodes.add(line[0])
            TSSDictionary[line[0]] = line[2]

# So that the outputfile will have the correct names
Abbreviations_Dict = {}
with open("abreviations.tsv") as abr:
    first_line = abr.readline()
    for x in abr:
        list = x.strip('\n').split('\t')
        if list[1] in RelevantTypes:
            Abbreviations_Dict[list[1]] = list[0]


file_name = sys.argv[1]
CancerPatientIDs = []

with open(sys.argv[1]) as input:
    AllPatients= [x for x in input.readline().strip('\n').split('\t') if x != '']
    CancerIndex = 0
    for x in AllPatients:
        if x.split('-')[1] in RelevantCodes:
            CancerPatientIDs.append(x)
            tss = x.split('-')[1]
            for Cancer in RelevantTypes:
                if TSSDictionary[tss] == Cancer:
                    CancerDict[Cancer].append(x)
    index_col = [line.split('\t')[0] for line in input]
print("Finished Step 1")

# df = pd.read_csv(sys.argv[1], delimiter='\t', usecols=CancerPatientIDs)[CancerPatientIDs]
# df = df.set_index("sample")
i = 0
for x in CancerDict:
    df = pd.read_csv(sys.argv[1], delimiter='\t', usecols=CancerDict[x], engine='c', na_values='NA')[CancerDict[x]].astype(float)
    s = pd.Series(index_col)
    s.name = ""
    df = pd.concat([s,df], axis=1)
    print(df.index)
    print(f'Finished Step 2.{i}')
    i+=1
    # y = y.loc[:, ~y.columns.duplicated()]
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
    df.to_csv(path_or_buf=('TCGA_' + Abbreviations_Dict[x] + '.ttsv'), sep='\t', na_rep="NA", index=False)
    print(f'Finished Evaluating TCGA_{Abbreviations_Dict[x]}')