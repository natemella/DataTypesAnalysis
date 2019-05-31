import os
import shutil
currentWorkingDir = os.path.dirname(os.path.realpath(__file__))


with open("CancerTypes.txt") as file:
    with open("abreviations.tsv") as abr:
        abreviations = [x.strip('\n') for x in file]
        RelevantTypes = [x.split('\t')[1].strip('\n') for x in abr if x.split('\t')[0] in abreviations]

# So that the outputfile will have the correct names
Abbreviations_Dict = {}
with open("abreviations.tsv") as abr:
    first_line = abr.readline()
    for x in abr:
        list = x.strip('\n').split('\t')
        if list[1] in RelevantTypes:
            Abbreviations_Dict["TCGA_" + list[0]] = list[1]



list = currentWorkingDir.split('/')
parent_directory = '/'.join(list[:-1])

# for CancerType, DataType, File in os.walk(parent_directory + '/InputData'):
#     print(CancerType)

for x in next(os.walk(parent_directory + "/InputData"))[1]:
    if x not in Abbreviations_Dict:
        shutil.rmtree(parent_directory + "/InputData/" + x)
        print(x)
