#!/usr/bin/env bash
#SBATCH -N 1 -n 8 --mem=16G -C rhel7
#SBATCH --array=0-0
#SBATCH --mail-user=nathanmell@gmail.com   # email address
#SBATCH --mail-type=END
#SBATCH --qos=test
#SBATCH --time=1:00:00   # walltime

. ./DataStandardization/functions.sh

endpoint=$1
numJobs=$2

echo WORKING

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

echo WORKING STEP 2

delay=0
jobLogFile=Analysis.job.log
dockerCommandsFile=Docker_Commands.sh
rm -f $jobLogFile
if [ -f $dockerCommandsFile ]
then
    rm $dockerCommandsFile
fi
cp -r InputData ../
for i in ${index_array[@]}; do
    ${ARRAY_OF_COMBINATIONS[$i]}
    execulte_analysis $dockerCommandsFile
    wait
done
echo WORKING STEP 3
while read line; do
    $line &
done < <(sed -n $(($SLURM_TASK_ARRAY_ID * $SLURM_NTASKS + 1)),$((($SLURM_TASK_ARRAY_ID + 1) * $SLURM_NTASKS))p $dockerCommandsFile)
wait
for i in ${index_array[@]}; do
    ${ARRAY_OF_COMBINATIONS[$i]}
    evaluate_results ${ARRAY_OF_ANALYSIS_NAMES[$i]}
done

rm -r *_Commands
