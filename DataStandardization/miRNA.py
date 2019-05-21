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
CancerPatientIDs = ['sample']


with open(sys.argv[1]) as input:
    AllPatients= input.readline().strip('\n').split('\t')
    CancerIndex = 0
    for x in AllPatients:
        if x.endswith("01") and x.split('-')[1] in RelevantCodes:
            CancerPatientIDs.append(x)
            tss = x.split('-')[1]
            for Cancer in RelevantTypes:
                if TSSDictionary[tss] == Cancer:
                    CancerDict[Cancer].append(x)


df = pd.read_csv(sys.argv[1], delimiter='\t', usecols=CancerPatientIDs)[CancerPatientIDs]
df = df.set_index("sample")
for x in CancerDict:
    y = df[CancerDict[x]].astype(int)
    y = y.groupby(level=0, axis=1).mean()
    # y = y.loc[:, ~y.columns.duplicated()]
    new_columns = []
    #truncate the IDs to twelve characters
    for ID in y.columns.values:
        truncatedID = ID[0:12]
        new_columns.append(truncatedID)
    y.columns = new_columns
    y.to_csv(path_or_buf=('TCGA_' + Abbreviations_Dict[x] + '.ttsv'), sep='\t', na_rep="NA")
