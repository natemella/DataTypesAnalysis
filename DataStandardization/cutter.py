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






my_list = path_to_list(currentWorkingDir)
parent_directory = sep_maker().join(my_list[:-1])

INPUT_DATA = next(os.walk(parent_directory + f"{sep_maker()}InputData"))[1]

# for unix it would be '{_}' for windows it would be '\'
_=sep_maker()

sample_summary = open("sample_summary.tsv",'w+')
sample_summary.write("CancerType\tOutcome\tNumber of Patients per type of Data\t"
                     "Total Number of Patients\t"
                     "Patients with all 7 types of data\n")

end_points = ["LT_PFI", "ST_PFI"]

for CancerType in INPUT_DATA:
    for outcome in end_points:
        sample_summary.write(f'{CancerType}\t')
        sample_summary.write(f'{outcome.replace("T_","")}\t')
        total_patients = set()
        patients_with_all = set()
        patients_per_data = []
        for list_of_dTypes in next(os.walk(os.path.join(*[parent_directory,"InputData",CancerType]))):
            already_seen = False
            if len(list_of_dTypes) > 1 and isinstance(list_of_dTypes, list):
                for DataType in list_of_dTypes:
                    d_type_directory = f"{parent_directory}{_}InputData{_}{CancerType}{_}{DataType}"
                    if DataType != "Class":
                        for input_file in os.listdir(d_type_directory):
                            if already_seen and DataType == "Covariate":
                                continue
                            input_file = f'{d_type_directory}{_}{input_file}'
                            if input_file.endswith(('.tsv','.txt')):
                                patients_per_data = [line.split('\t')[0] for line in open(input_file)]
                                patients_per_data.pop(0)
                                sample_summary.write(f'{DataType}:{len(set(patients_per_data))}|')
                                total_patients.update(patients_per_data)
                                patients_with_all.intersection(set(patients_per_data))
                            else:
                                with codecs.open(input_file, 'r') as myfile:
                                    firstline = myfile.readline()
                                    patients_per_data = firstline.split('\t')
                                    patients_per_data.pop(0)
                                    sample_summary.write(f'{DataType}:{len(set(patients_per_data))}|')
                                    total_patients.update(patients_per_data)
                                    patients_with_all.intersection((set(patients_per_data)))
                            if DataType == "Covariate":
                                already_seen = True
                    else:
                        patients_per_data = [line.split('\t')[0] for line in open(f'{d_type_directory}{_}PFI.txt') if line.strip('\n').split('\t')[1] == outcome]
                        patients_per_data.pop(0)
                        patients_with_all.update(patients_per_data)
                        sample_summary.write(f'{DataType}:{len(patients_with_all)}|')
        sample_summary.write(f'\t{len(total_patients)}\t{len(patients_with_all)}\n')
sample_summary.close()