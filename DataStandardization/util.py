import os


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


def path_delimiter():
    Folders = ['a', 'b']
    x = os.path.join(*Folders)
    return x[1]

def make_relevant_types_list():
    with open("CancerTypes.txt") as file:
        with open("abreviations.tsv") as abr:
            abreviations = [x.strip('\n') for x in file]
            relevant_types = [x.split('\t')[1].strip('\n') for x in abr if x.split('\t')[0] in abreviations]
    return relevant_types

def make_cancer_dict(relevant_types):
    cancer_dict = {}
    for x in relevant_types:
        cancer_dict[x] = []
    return cancer_dict

def make_tss_dict_and_rev_codes_dic(relevant_types):
    relevant_codes = set()
    tss_dictionary = {}
    with open("TSS_CODES.tsv") as codes:
        codes.readline()
        for x in codes:
            line = x.strip('\n').split('\t')
            if line[2] in relevant_types:
                relevant_codes.add(line[0])
                tss_dictionary[line[0]] = line[2]
    return [relevant_codes, tss_dictionary]

def make_abbrevation_dict(relevant_types):
    abbreviations_dict = {}
    with open("abreviations.tsv") as abr:
        abr.readline()
        for x in abr:
            list = x.strip('\n').split('\t')
            if list[1] in relevant_types:
                abbreviations_dict[list[1]] = list[0]
    return abbreviations_dict

def fill_cancer_dict(relevant_codes, tss_dictionary, cancer_dict, relevant_types, all_patients):
    cancer_patient_ids = []

    for sample_id in all_patients:
        if sample_id.split('-')[1] in relevant_codes:
            cancer_patient_ids.append(sample_id)
            tss = sample_id.split('-')[1]
            for Cancer in relevant_types:
                if tss_dictionary[tss] == Cancer:
                    cancer_dict[Cancer].append(sample_id)

def dictionary_makers(all_patients):

    relevant_types = make_relevant_types_list()
    cancer_dict = make_cancer_dict(relevant_types)
    relevant_codes = make_tss_dict_and_rev_codes_dic(relevant_types)[0]
    tss_dictionary = make_tss_dict_and_rev_codes_dic(relevant_types)[1]
    abbreviations_dict = make_abbrevation_dict(relevant_types)
    cancer_patient_ids = (relevant_codes, tss_dictionary, cancer_dict, relevant_types, all_patients)

    return [relevant_types, relevant_codes, tss_dictionary, abbreviations_dict, cancer_dict, cancer_patient_ids]
