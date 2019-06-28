#!/usr/bin/env bash
. ./DataStandardization/functions.sh

endpoint=$1
numJobs=$2

if [ ! -f "InputData/TCGA_UCEC/Clinical/TCGA_UCEC_"$endpoint"_cut.tsv" ]
then
    if [ -f InputData/TCGA_UCEC/Clinical/TCGA_UCEC.tsv ]
    then
        cd DataStandardization/
        python3 cutter.py -c True -e $endpoint
        bash scale_ohe_impute.sh
        cd ../
    else
        cd DataStandardization/
        bash download_and_parse_all_data.sh $endpoint
        cd ../
    fi
fi

no_combination() {
python3 create_data_to_process_files.py $endpoint
}

add_clinical() {
python3 create_data_to_process_files.py $endpoint -c True
}

add_miRNA() {
python3 create_data_to_process_files.py $endpoint -c True -m True
}

add_RPPA() {
python3 create_data_to_process_files.py $endpoint -c True -m True -p True
}

add_SM() {
python3 create_data_to_process_files.py $endpoint -c True -m True -p True -s True
}

add_CNV() {
python3 create_data_to_process_files.py $endpoint -c True -m True -p True -s True -n True
}

add_dna_methylation() {
python3 create_data_to_process_files.py $endpoint -c True -m True -p True -s True -n True -e True
}

declare -a ARRAY_OF_COMBINATIONS
declare -a ARRAY_OF_ANALYSIS_NAMES

ARRAY_OF_COMBINATIONS=(no_combination add_clinical add_miRNA add_RPPA add_SM add_CNV add_dna_methylation)
ARRAY_OF_ANALYSIS_NAMES=("no_combination" "+clinical" "+clinical+miRNA" "+clinical+miRNA+RPPA" "+SM" "add_CNV" "add_dna_methylation")
index_array=(0 1 2 3 4 5 6)

delay=1
jobLogFile=Analysis.job.log
dockerCommandsFile=Docker_Commands.sh
rm -f $jobLogFile
if [ -f $dockerCommandsFile ]
then
    rm $dockerCommandsFile
fi
for i in ${index_array[@]}; do
    ${ARRAY_OF_COMBINATIONS[$i]}
    execulte_analysis $dockerCommandsFile
done
parallel --retries 0 --shuf --progress --eta --delay $delay --joblog $jobLogFile -j $numJobs -- < $dockerCommandsFile
for i in ${index_array[@]}; do
    ${ARRAY_OF_COMBINATIONS[$i]}
    evaluate_results ${ARRAY_OF_ANALYSIS_NAMES[$i]}
done

rm -r *_Commands
