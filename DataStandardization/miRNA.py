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
for x in CancerDict:
    CancerDict[x].append('sample')


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
Duplicate_Indexes = {}

with open(sys.argv[1]) as input:
    AllPatients= input.readline().strip('\n').split('\t')
    CancerIndex = 0
    for x in AllPatients:
        if x in CancerPatientIDs:
            first_duplicate = CancerPatientIDs.index(x)
            second_duplicate = CancerIndex
            Duplicate_Indexes[first_duplicate] = second_duplicate
        if x.endswith("01") and x.split('-')[1] in RelevantCodes:
            CancerPatientIDs.append(x)
            tss = x.split('-')[1]
            for Cancer in RelevantTypes:
                if TSSDictionary[tss] == Cancer:
                    CancerDict[Cancer].append(x)


df = pd.read_csv(sys.argv[1], delimiter='\t', usecols=CancerPatientIDs)[CancerPatientIDs]

#take out repeats
for x in Duplicate_Indexes:
    val1 = x
    val2 = Duplicate_Indexes[x]
    print("First duplicate = " + CancerPatientIDs[val1] + " occured at index " + str(val1))
    print("Second duplicate = " + CancerPatientIDs[val2] + " occured at index " + str(val2))
    duplicate_df = df[CancerPatientIDs[x]] # grab the columns that repeat
    series = duplicate_df.mean(axis=1) # average the duplicate values together
    temp_df = pd.DataFrame({CancerPatientIDs[x]:series.values}) #turn the series into a DataFrame
    df = df.drop(labels=[CancerPatientIDs[x]], axis=1) # take out all of the duplicate columns
    df = pd.concat([df,temp_df], axis=1) # concate the average of the duplicate columns

df_index = pd.read_csv(sys.argv[1], delimiter='\t', usecols=['sample'])
df = pd.concat([df_index,df], axis=1)
for x in CancerDict:
    y = df[CancerDict[x]]
    i = 0
    #truncate the IDs to twelve characters
    for ID in CancerDict[x]:
        if ID == 'sample':
            i += 1
            continue
        truncatedID = ID[0:12]
        CancerDict[x][i] = truncatedID
        i +=1
    y.columns = CancerDict[x]
    y.to_csv(path_or_buf=('TCGA_' + Abbreviations_Dict[x] + '.ttsv'), sep='\t', index=False)
