#!/usr/bin/env bash
#SBATCH -N 1 -n 8 --mem=32G -C rhel7
#SBATCH --array=0-256
#SBATCH --mail-user=nathanmell@gmail.com   # email address
#SBATCH --mail-type=END
#SBATCH --time=12:00:00   # walltime
set -u
. ./DataStandardization/functions.sh

endpoint=$1

echo *****************************************
echo CHECKING WHETHER DATA HAS BEEN DOWNLOADED
echo *****************************************

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

new_combo() {
counter=$1
if [ $counter -eq 0 ] ; then
    echo ${endpoint}
else
    echo $(python3 get_combo.py $(new_combo $(($counter-1))))
fi
}

index_array=(0 1 2 3 4 5 6)


delay=0
jobLogFile=Analysis.job.log
dockerCommandsFile=Docker_Commands.sh
rm -f $jobLogFile
cp -r InputData ../
for i in ${index_array[@]}; do
    if [ -e $dockerCommandsFile ]; then
        rm $dockerCommandsFile
    fi
    python3 create_data_to_process_files.py $(new_combo $i)
    echo *****************************************
    echo MAKING TEMPORARY COMMAND FILES
    echo *****************************************
    execulte_analysis $dockerCommandsFile
    wait
    echo *****************************************
    echo RUNNING $(python3 get_analysis_name $(new_combo $i)) ANALYSIS COMMANDS
    echo *****************************************
    while read line; do
        $line &
    done < <(sed -n $(($SLURM_ARRAY_TASK_ID * $SLURM_NTASKS + 1)),$((($SLURM_ARRAY_TASK_ID + 1) * $SLURM_NTASKS))p $dockerCommandsFile)
    wait
    echo *****************************************
    echo EVALUATING RESULTS FOR $(python3 get_analysis_name $(new_combo $i))
    echo *****************************************
    evaluate_results $(python3 get_analysis_name $(new_combo $i))
    rm -r *_Commands
done

