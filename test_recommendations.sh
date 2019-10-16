#!/usr/bin/env bash
set -u

endpoint=${1:-PFI}
slurm_environment=${2:-True}
number_of_cores=${3:-2}

echo Parameters are:
echo endpoint = $endpoint
echo slurm environment = $slurm_environment
echo number of cores = $number_of_cores


#Insert all functions

evaluate_results() {
experiment_name=$1
new_output=${experiment_name}".tsv"
new_predictions=${experiment_name}"_Predictions.tsv.gz"
search_dir=Data_To_Process_Files

ARRAY=()
for dir in $(ls $search_dir); do
    for file in $(ls $search_dir/$dir); do
        ARRAY+=(${dir}"_"${file})
    done
done

for dir in `ls $search_dir`; do
    for file in $(ls $search_dir/$dir); do
        IFS='.' read -ra Analysis <<< "$file"
        datafile=${search_dir}/${dir}/${file}
        analysis="${Analysis[0]}"
        IFS='+' read -ra trial <<< "$analysis"
        python3 get_metrics.py $datafile
        output=${dir}_${analysis}".tsv"
        cd Analysis_Results
        if [[ ${dir}"_"${file} == "${ARRAY[0]}" ]];
        then
            cat $output >> $new_output
        else
            tail -n +2 $output >> $new_output
        fi
        cd ../
    done
done

cd Analysis_Results
mv "Total_Predictions.tsv.gz" $new_predictions
mv $new_output ../
mv $new_predictions ../
cd ../
if [ -d Permanent_Results/ ]
then
    mv $new_output $new_predictions Permanent_Results/
else
    mkdir Permanent_Results
    mv $new_output $new_predictions Permanent_Results/
fi
cd Analysis_Results
rm *__*.t*
cd ../
}

execute_analysis() {
search_dir=Data_To_Process_Files
dockerCommandsFile=${1-Docker_Commands.sh}
slurm_environment=${2:-True}
number_of_cores=${3:-2}
for dir in `ls $search_dir`; do
    for file in $(ls $search_dir/$dir); do
        datafile=${search_dir}/${dir}/${file}
        python3 create_temporary_bash_scripts.py $datafile -z ${slurm_environment} -c ${number_of_cores}
    done
done
}

check_if_all_commands_finished() {
inputfile=$1
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

build_parameters() {
i=$1
for algorithm_path in $(cat Algorithms.txt); do
    algorithm_path="${algorithm_path/AlgorithmScripts\/Classification\//}"
    algorithm_path="${algorithm_path/\//__}"
    algorithm_path="${algorithm_path/\//__}"
    algorithm_path="${algorithm_path/\//}"
    algorithm=${algorithm_path}
    python3 recommendation_tester.py $algorithm $endpoint $i
done
}
#Remove existing analysis results
cd Analysis_Results/
if [ -f *.tsv ]
then
    rm *.tsv
fi
cd ../


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

cd ../
if [ ! -d "InputData/" ]; then
    cd DataTypesAnalysis
    echo "########################################"
    echo COPYING INPUTDATA TO CORRECT LOCATION
    echo "########################################"
    cp -r InputData ../
else
    cd DataTypesAnalysis
fi

index_array=(0 1 2 3 4 5 6)

delay=0
jobLogFile=Analysis.job.log
dockerCommandsFile=Docker_Commands.sh
rm -f $jobLogFile

for i in ${index_array[@]}; do
    if [ -e $dockerCommandsFile ]; then
        rm $dockerCommandsFile
    fi
    build_parameters $i
    echo "########################################"
    echo MAKING TEMPORARY HYPOTHESIS COMMAND FILES
    echo "########################################"
    execute_analysis $dockerCommandsFile $slurm_environment
    echo "########################################"
    echo RUNNING COMBINATIONS OF $i ANALYSIS COMMANDS HYPOTHESIS TESTING MODE
    echo "########################################"
    if [ -e $dockerCommandsFile ]; then
        if [[ $slurm_environment == "True" ]]; then
            num_of_commands=$(wc -l < $dockerCommandsFile)
            python3 build_job_array.py $num_of_commands
            if [ $num_of_commands -ne 0 ]; then
                sbatch --wait job_array.sh $dockerCommandsFile
                count=2
                while [ -e "job_array$count.sh" ]
                do
                    sbatch --wait "job_array$count.sh" $dockerCommandsFile
                    count=$((count+1))
                done
            fi
        else
            delay=1
            numJobs=7
            jobLogFile=Analysis.job.log
            rm -f $jobLogFile
            cat $dockerCommandsFile
            parallel --retries 0 --shuf --progress --eta --delay $delay --joblog $jobLogFile -j $numJobs -- < $dockerCommandsFile
        fi

        if [ -e $dockerCommandsFile ]; then
            rm $dockerCommandsFile
        fi
    fi

    echo "########################################"
    echo EVALUATING RESULTS FOR COMBINATIONS OF $i
    echo "########################################"
    evaluate_results "test_hypothesis_combination_of_"${i}
    execute_analysis $dockerCommandsFile $slurm_environment
    if [ -e $dockerCommandsFile ]; then
        check_if_all_commands_finished $dockerCommandsFile
    else
        echo SUCCESS, ALL COMMANDS SUCCESSFULLY FINISHED!!!!
        echo BEGINNING NEXT COMBINATION OF DATA TYPES!!!
    fi
done