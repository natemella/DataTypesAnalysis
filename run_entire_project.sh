#!/usr/bin/env bash
. ./DataStandardization/functions.sh

endpoint=$1

if [ ! -f InputData/TCGA_UCEC/Clinical/TCGA_UCEC_cut.tsv ]
then
    bash DataStandardization/download_and_parse_all_data.sh $endpoint
fi

no_combination() {
python3 create_data_to_process_files.py PFI
}

add_clinical() {
python3 create_data_to_process_files.py PFI -c True
}

add_miRNA() {
python3 create_data_to_process_files.py PFI -c True -m True
}

add_RPPA() {
python3 create_data_to_process_files.py PFI -c True -m True -p True
}

add_SM() {
python3 create_data_to_process_files.py PFI -c True -m True -p True -s True
}

add_CNV() {
python3 create_data_to_process_files.py PFI -c True -m True -p True -s True -n True
}

add_dna_methylation() {
python3 create_data_to_process_files.py PFI -c True -m True -p True -s True -n True -e True
}

declare -a ARRAY_OF_COMBINATIONS
declare -a ARRAY_OF_ANALYSIS_NAMES

ARRAY_OF_COMBINATIONS=(no_combination add_clinical add_miRNA add_RPPA add_SM add_CNV add_dna_methylation)
ARRAY_OF_ANALYSIS_NAMES=("no_combination" "+clinical" "+clinical+miRNA" "+clinical+miRNA+RPPA" "+SM" "add_CNV" "add_dna_methylation")
index_array=(0 1 2 3 4 5 6)

for i in ${index_array[@]}; do
    ${ARRAY_OF_COMBINATIONS[$i]}
    execulte_analysis
    evaluate_results ${ARRAY_OF_ANALYSIS_NAMES[$i]}
done
rm -r *_Commands
