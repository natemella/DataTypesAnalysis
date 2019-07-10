#!/usr/bin/env bash
set -u
. ./DataStandardization/functions.sh

endpoint=$1

echo "########################################"
echo CHECKING WHETHER DATA HAS BEEN DOWNLOADED
echo "########################################"

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

check_if_all_commands_finished() {
inputfile=$1
execute_analysis ${inputfile}
num_of_commands=$(wc -l < ${inputfile})
if [ $num_of_commands -ne 0 ]; then
    echo THE FOLLOWING COMMANDS FAILED TO COMPLETE:
    cat ${inputfile}
    echo THIS PROGRAM WILL THEREFORE EXIT
    rm -rf *_Commands
    exit
else
    echo SUCCESS, ALL COMMANDS SUCCESSFULLY FINISHED!!!!
    echo BEGINNING NEXT COMBINATION OF DATA TYPES!!!
    rm -rf *_Commands
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
    echo "########################################"
    echo MAKING TEMPORARY COMMAND FILES
    echo "########################################"
    execute_analysis $dockerCommandsFile
    num_of_commands=$(wc -l < $dockerCommandsFile)
    python3 build_job_array.py $num_of_commands
    if [ $num_of_commands -ne 0 ]; then
        sbatch --wait job_array.sh $dockerCommandsFile
    fi
    echo "########################################"
    echo RUNNING $(python3 get_analysis_name.py $(new_combo $i)) ANALYSIS COMMANDS
    echo "########################################"
    rm $dockerCommandsFile
    python3 create_data_to_process_files.py $(new_combo $i)
    echo "########################################"
    echo EVALUATING RESULTS FOR $(python3 get_analysis_name.py $(new_combo $i))
    echo "########################################"
    evaluate_results $(python3 get_analysis_name.py $(new_combo $i))
    check_if_all_commands_finished $dockerCommandsFile
done

