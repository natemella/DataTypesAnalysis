import pandas as pd
import sys
PatientID = []
Check = {}
duplicate_indexes = []
with open(sys.argv[1]) as input:
    first_line = input.readline()
    first_line = first_line.strip('\n')
    Input = first_line.split('\t')
    index = 0
    for x in Input:
        if x in PatientID:
            myint = PatientID.index(x)
            print()
            print(PatientID[myint])
            duplicate_indexes.append(PatientID.index(x))
            duplicate_indexes.append(index)
        if x.endswith("01"):
            PatientID.append(x)
        index +=1
df = pd.read_csv(sys.argv[1], delimiter='\t', usecols=PatientID)

for x in duplicate_indexes:
    Check[x] = df[PatientID[x]]
# print(df)
    print(PatientID[x])