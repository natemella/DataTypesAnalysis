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
    Header = input.readline().split('\t')
    AllPatients = [x.split('\t')[0] for x in input]
    for x in AllPatients:
        if x.endswith("01"):
            CancerPatientIDs.append(x)
            if x.split('-')[1] in RelevantCodes:
                tss = x.split('-')[1]
                for Cancer in RelevantTypes:
                    if TSSDictionary[tss] == Cancer:
                        CancerDict[Cancer].append(x)

df = pd.read_csv("TCGA-RPPA-pancan-clean.xena", sep="\t", index_col="SampleID")
df = df.loc[CancerPatientIDs]
df = df.groupby(['SampleID']).mean()

Protein_NA_info = df.describe()
columns = Protein_NA_info.columns.values.tolist()
proteins_to_drop = []
proteins_to_keep = []
Tumors_to_drop = []
Tumors_to_keep = []

# filter out proteins if less than 20%
for i in columns:
    Na_count = len(df.index) - Protein_NA_info[i][0]
    percent_missing = Na_count/len(df.index)
    if percent_missing > 0.2:
        proteins_to_drop.append(i)
    else:
        proteins_to_keep.append(i)

print("Proteins removed = " + str(len(proteins_to_drop)))

info = df.count(axis=1)
for key, value in info.iteritems():
    count = len(df.columns.values) - value
    percent_missing = count/len(df.columns.values)
    if percent_missing > 0.2:
        Tumors_to_drop.append(key)
    else:
        Tumors_to_keep.append(key)

print("Tumors removed = " + str(len(Tumors_to_drop)))
# df.drop(labels=indexes_to_drop, axis=1)
df = df[proteins_to_keep]
df = df.loc[Tumors_to_keep]

# convert NaN to NA

a = df.columns.values.tolist()
for x in proteins_to_drop:
    if x in a:
        print("fail")
for x in CancerDict:
    y = df.loc[CancerDict[x]]
    i = 0
    #truncate the IDs to twelve characters
    for ID in CancerDict[x]:
        if ID == 'SampleID':
            i += 1
            continue
        truncatedID = ID[0:12]
        CancerDict[x][i] = truncatedID
        i +=1

    y.index = CancerDict[x]
    y.to_csv(path_or_buf=('TCGA_' + Abbreviations_Dict[x] + '.tsv'), sep='\t', na_rep='NA')