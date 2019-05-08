import pandas as pd
import sys

RelevantTypes = ("Glioblastoma multiforme","Ovarian serous cystadenocarcinoma", "Lung squamous cell carcinoma",
                 "Breast invasive carcinoma","Lung adenocarcinoma", "Prostate adenocarcinoma",
                 "Skin Cutaneous Melanoma", "Colon adenocarcinoma", "Bladder Urothelial Carcinoma", "Sarcoma", "Kidney renal clear cell carcinoma")
#to get a map for all of the TSS codes to each cancer type
TSSDictionary = {}

#to make a data frame for each cancer type
CancerDict = {"Glioblastoma multiforme": [],"Ovarian serous cystadenocarcinoma" : [], "Lung squamous cell carcinoma":[],
                 "Breast invasive carcinoma":[],"Lung adenocarcinoma": [], "Prostate adenocarcinoma" : [],
                 "Skin Cutaneous Melanoma": [], "Colon adenocarcinoma": [], "Bladder Urothelial Carcinoma": [], "Sarcoma": [],
              "Kidney renal clear cell carcinoma": []}

RelevantCodes = set()



GM = "Glioblastoma multiforme"
OSC = "Ovarian serous cystadenocarcinoma"
LS = "Lung squamous cell carcinoma"
BC = "Breast invasive carcinoma"
LA = "Lung adenocarcinoma"
PA = "Prostate adenocarcinoma"
SC = "Skin Cutaneous Melanoma"
CA = "Colon adenocarcinoma"
BUC = "Bladder Urothelial Carcinoma"
S = "Sarcoma"
KIRC = "Kidney renal clear cell carcinoma"


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
    Header = input.readline().split('\t')
    AllPatients = [x.split('\t')[0] for x in input]
    CancerIndex = 0
    for x in AllPatients:
        if x in CancerPatientIDs:
            first_duplicate = CancerPatientIDs.index(x)
            second_duplicate = CancerIndex
            Duplicate_Indexes[first_duplicate] = second_duplicate
        if x.endswith("01") and x.split('-')[1] in RelevantCodes:
            CancerPatientIDs.append(x)
            tss = x.split('-')[1]
            if TSSDictionary[tss] == GM:
                CancerDict[GM].append(x)
            elif TSSDictionary[tss] == OSC:
                CancerDict[OSC].append(x)
            elif TSSDictionary[tss] == BC:
                CancerDict[BC].append(x)
            elif TSSDictionary[tss] == LA:
                CancerDict[LA].append(x)
            elif TSSDictionary[tss] == PA:
                CancerDict[PA].append(x)
            elif TSSDictionary[tss] == SC:
                CancerDict[SC].append(x)
            elif TSSDictionary[tss] == CA:
                CancerDict[CA].append(x)
            elif TSSDictionary[tss] == BUC:
                CancerDict[BUC].append(x)
            elif TSSDictionary[tss] == S:
                CancerDict[S].append(x)
            elif TSSDictionary[tss] == KIRC:
                CancerDict[S].append(x)
            CancerIndex +=1

df = pd.read_csv("TCGA-RPPA-pancan-clean.xena", sep="\t", index_col="SampleID")
df = df.groupby(['SampleID']).mean()

#
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
    y.to_csv(path_or_buf=('TCGA_' + Abbreviations_Dict[x] + '.tsv'), sep='\t')