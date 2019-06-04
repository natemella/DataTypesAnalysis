import os
import sys
currentWorkingDir = os.path.dirname(os.path.realpath(__file__))
import codecs

RelevantTypes = ()

def path_to_list(path):
  folders = []
  while True:
    path, folder = os.path.split(path)
    if folder:
      folders.append(folder)
    else:
      if path:
        folders.append(path)
      break
  folders.reverse()
  return folders

def sep_maker():
  list = ['a','b']
  x = os.path.join(*list)
  return x[1]





endpoints = sys.argv[1:]


my_list = path_to_list(currentWorkingDir)
parent_directory = sep_maker().join(my_list[:-1])

INPUT_DATA = next(os.walk(parent_directory + f"{sep_maker()}InputData"))[1]

# for unix it would be '{_}' for windows it would be '\'
_=sep_maker()

sample_summary = open("sample_summary.tsv",'w+')
sample_summary.write("CancerType\tNumber of Patients per type of Data\t"
                     "Total Number of Patients\t"
                     "Patients with all 7 types of data\n")
total_patients = set()
patients_with_all = set()
patients_per_data = []

for CancerType in INPUT_DATA:
    sample_summary.write(f'{CancerType}\t')
    for list_of_dTypes in next(os.walk(os.path.join(*[parent_directory,"InputData",CancerType]))):
        if len(list_of_dTypes) > 1 and isinstance(list_of_dTypes, list):
            for DataType in list_of_dTypes:
                d_type_directory = f"{parent_directory}{_}InputData{_}{CancerType}{_}{DataType}"
                if DataType == "Covariate":
                    continue
                if DataType != "Class":
                    for input_file in os.listdir(d_type_directory):
                        input_file = f'{d_type_directory}{_}{input_file}'
                        if input_file.endswith(('.tsv','.txt')):
                            patients_per_data = [line.split('\t')[0] for line in open(input_file)].pop(0)
                            print(patients_per_data)
                            sample_summary.write(f'{DataType}:{len(patients_per_data)}|')
                            total_patients.update(patients_per_data)
                            patients_with_all.intersection(set(patients_per_data))
                        else:
                            with codecs.open(input_file, 'r', encoding="utf-8", errors="ignore") as myfile:
                                firstline = myfile.readline()
                                patients_per_data = firstline.split('\t').pop(0)
                                print(patients_per_data)
                                sample_summary.write(f'{DataType}:{len(patients_per_data)}')
                                total_patients.update(patients_per_data)
                                patients_with_all.intersection((set(patients_per_data)))
                else:
                    patients_with_all.update(line.split('\t')[0] for line in open(f'{d_type_directory}{_}PFI.txt'))
    sample_summary.write(f'{len(total_patients)}\t{len(patients_with_all)}\n')
sample_summary.close()