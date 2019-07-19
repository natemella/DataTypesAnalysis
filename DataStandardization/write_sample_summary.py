import os
import codecs
from util import *
import sys


Analysis_endpoint = sys.argv[1]

# get path to input data folders
currentWorkingDir = os.getcwd()
parent_folders = path_to_list(currentWorkingDir)
parent_directory = path_delimiter().join(parent_folders[:-1])
input_data_dir = next(os.walk(os.path.join(*[parent_directory, "InputData"])))[1]

# for unix it would be '{_}' for windows it would be '\'
_=path_delimiter()

# write header of sample_summary file
sample_summary = open("sample_summary.csv",'w+')
sample_summary.write("CancerType,Outcome,Class,Clinical,CNV,Covariate,DNA_Methylation,Expression,miRNA,RPPA,SM,Total\n")

end_points = [f"LT_{Analysis_endpoint}", f"ST_{Analysis_endpoint}"]
for CancerType in sorted(input_data_dir):

    # This for loop below is to separate Long Term {endpoint} from Short Term {endpoint}
    for outcome in end_points:

        sample_summary.write(f'{CancerType},')
        sample_summary.write(f'{outcome.replace("T_", "")},')

        patients_with_all_data_types = set()
        class_info = set()
        patients_per_data_type = []
        cancer_path = os.path.join(*[parent_directory, "InputData", CancerType])
        data_paths = []

        for DataType in sorted(os.listdir(cancer_path), key=lambda s: s.lower()):

            data_type_path = os.path.join(*[parent_directory, "InputData", CancerType, DataType])
            data_paths.append(data_type_path)

            if DataType != "Class":
                for input_file in (os.listdir(data_type_path)):
                    # we don't want to re-cut an already cut file
                    if is_cut_or_tempfile(input_file):
                        continue

                    input_file = f'{data_type_path}{_}{input_file}'
                    # In TSV files, patient ID's are the first word of each line
                    if input_file.endswith(('.tsv','.txt')):
                        patients_per_data_type = [line.split('\t')[0] for line in open(input_file)]
                        patients_with_all_data_types = patients_with_all_data_types.intersection(set(patients_per_data_type))
                        sample_summary.write(f'{len(class_info.intersection(patients_per_data_type))}')
                    else:
                        # In TTSV files, patient ID's are the first line
                        with codecs.open(input_file, 'r') as myfile:
                            firstline = myfile.readline()
                            patients_per_data_type = firstline.split('\t')
                            patients_with_all_data_types = patients_with_all_data_types.intersection(set(patients_per_data_type))
                            sample_summary.write(f'{len(class_info.intersection(patients_per_data_type))}')

            # We expect to open the Class files first since Class comes alphabetically before Clinical, Covariate, CNV, DNA_Methylation, Expression, miRNA, RPPA, and SM
            # This is where we begin to build our set of patients with all_data_types
            else:
                patients_per_data_type = [line.split('\t')[0] for line in open(f'{data_type_path}{_}{Analysis_endpoint}.tsv') if line.strip('\n').split('\t')[1] == outcome]
                patients_with_all_data_types.update(patients_per_data_type)
                class_info.update(patients_per_data_type)
                sample_summary.write(f'{DataType}:{len(patients_with_all_data_types)},')

            sample_summary.write(' | ')
        sample_summary.write(f',{len(patients_with_all_data_types)}\n')

sample_summary.close()