import pandas as pd

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

CancerPatientIDs = []

with open("mmc1.xlsx.CSV") as input:
    Header = input.readline().split(',')
    AllPatients = [x.split(',')[1] for x in input]
    for x in AllPatients:
        if x.split('-')[1] in RelevantCodes:
            CancerPatientIDs.append(x)
            tss = x.split('-')[1]
            for Cancer in RelevantTypes:
                if TSSDictionary[tss] == Cancer:
                    CancerDict[Cancer].append(x)

df = pd.read_csv("mmc1.xlsx.CSV", sep=",", index_col="bcr_patient_barcode")
df = df.drop(labels="Unnamed: 0", axis=1)

df = df.loc[CancerPatientIDs]

endpoints = ("DFI","DSS","OS","PFI")

output = open("Covariate_log.out",'w')

for x in CancerDict:
    output.write(f"Generating File for {x}\n")
    y = df.loc[CancerDict[x]]

    info = y.describe(include="all")
    columns = info.columns.values
    variables_to_keep = []
    variables_to_drop = []

    output.write(f'\nTotal columns:\n{columns}\n\n')
    for i in columns:
        if i.startswith(endpoints):
            variables_to_keep.append(i)
            continue
        Na_count = len(y.index) - info[i][0]
        percent_missing = Na_count / len(y.index)
        if percent_missing > 0.2:
            variables_to_drop.append(i)
        else:
            variables_to_keep.append(i)




    output.write(f'variables to keep for {x}: {variables_to_keep}\n')
    output.write(f'variables to drop to drop for {x}: {variables_to_drop}\n\n')
    y = y[variables_to_keep]
    y.to_csv(path_or_buf=('TCGA_' + Abbreviations_Dict[x] + '.tsv'), sep='\t', na_rep='NA')
output.close()
