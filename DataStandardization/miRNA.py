import pandas as pd
import sys

RelevantTypes = ("Glioblastoma multiforme","Ovarian serous cystadenocarcinoma", "Lung squamous cell carcinoma",
                 "Breast invasive carcinoma","Lung adenocarcinoma", "Prostate adenocarcinoma",
                 "Skin Cutaneous Melanoma", "Colon adenocarcinoma", "Bladder Urothelial Carcinoma", "Sarcoma", "Kidney renal clear cell carcinoma")
TSSDictionary = {}
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

for x in CancerDict:
    df[CancerDict[x]].to_csv(path_or_buf=('TCGA_' + Abbreviations_Dict[x] + '.ttsv'), sep='\t')
