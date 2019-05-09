import os
import shutil
currentWorkingDir = os.path.dirname(os.path.realpath(__file__))

RelevantTypes = ()

# RelevantTypes = ("Glioblastoma multiforme","Ovarian serous cystadenocarcinoma", "Lung squamous cell carcinoma",
#                  "Breast invasive carcinoma","Lung adenocarcinoma", "Prostate adenocarcinoma",
#                  "Skin Cutaneous Melanoma", "Colon adenocarcinoma", "Bladder Urothelial Carcinoma", "Sarcoma",
#                  "Kidney renal clear cell carcinoma")



# So that the outputfile will have the correct names
Abbreviations_Dict = {}
with open("abreviations.tsv") as abr:
    first_line = abr.readline()
    for x in abr:
        list = x.strip('\n').split('\t')
        if list[1] in RelevantTypes:
            Abbreviations_Dict["TCGA_" + list[0]] = list[1]


for x in Abbreviations_Dict:
    print(x)

list = currentWorkingDir.split('/')
parent_directory = '/'.join(list[:-1])
print("parent directory = " + parent_directory)
print("current directory = " + currentWorkingDir)

# for CancerType, DataType, File in os.walk(parent_directory + '/InputData'):
#     print(CancerType)

print(next(os.walk(parent_directory + "/InputData"))[1])
for x in next(os.walk(parent_directory + "/InputData"))[1]:
    if x not in Abbreviations_Dict and "Class" not in next(os.walk(parent_directory + "/InputData/" + x))[1]:
        shutil.rmtree(parent_directory + "/InputData/" + x)
