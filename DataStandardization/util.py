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


def dictionary_makers(all_patients):
    with open("CancerTypes.txt") as file:
        with open("abreviations.tsv") as abr:
            abreviations = [x.strip('\n') for x in file]
            relevant_types = [x.split('\t')[1].strip('\n') for x in abr if x.split('\t')[0] in abreviations]

    cancer_dict = {}
    for x in relevant_types:
        cancer_dict[x] = []

    relevant_codes = set()


    tss_dictionary = {}
    with open("TSS_CODES.tsv") as codes:
        codes.readline()
        for x in codes:
            line = x.strip('\n').split('\t')
            if line[2] in relevant_types:
                relevant_codes.add(line[0])
                tss_dictionary[line[0]] = line[2]

    # So that the outputfile will have the correct names
    abbreviations_dict = {}
    with open("abreviations.tsv") as abr:
        abr.readline()
        for x in abr:
            list = x.strip('\n').split('\t')
            if list[1] in relevant_types:
                abbreviations_dict[list[1]] = list[0]

    cancer_patient_ids = []

    for sample_id in all_patients:
        if sample_id.split('-')[1] in relevant_codes:
            cancer_patient_ids.append(sample_id)
            tss = sample_id.split('-')[1]
            for Cancer in relevant_types:
                if tss_dictionary[tss] == Cancer:
                    cancer_dict[Cancer].append(sample_id)

    return [relevant_types, relevant_codes, tss_dictionary, abbreviations_dict, cancer_dict, cancer_patient_ids]
