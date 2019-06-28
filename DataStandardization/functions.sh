#!/usr/bin/env bash
set -a # export all functions
set -e

rename_if_necessary() {
    fileName=$1
    rename=$2
    extension=$3
    if [[ $rename == "True" ]];
    then
        mv $fileName ${fileName}${extension}
        echo ${fileName}${extension}
    else
        echo ${fileName}
    fi
}

gunzip_if_gzipped() {
fileName=$1
if [[ $fileName =~ \.gz$ ]];
then
    gunzip ${fileName}
    echo ${fileName//.gz/}
else
    echo ${fileName}
fi
}

check_if_file_already_exits() {
filepath=$1
force=$2
if [[ $force -ne "-f" ]]
then
    if [ -f ${filepath} ]
    then
        echo Already Downloaded
        exit 1
    fi
fi

}
download_and_organize_data() {
fileName=$1
python_script=$2
web_url=$3
tcga_extension=$4
folder=$5
file_extension=$6
rename=$7
force=$8

file_to_check="../InputData/TCGA_BRCA/"${folder}"/*"${tcga_extension}
check_if_file_already_exits ${file_to_check} $force

if [ -e $fileName* ]
then
    echo Beginning to run ${python_script}
    python3 $python_script $fileName
    echo ${fileName}
else
    echo $fileName has not yest been downloaded
    wget ${web_url}/${fileName}
    fileName=$(rename_if_necessary ${fileName} ${rename} ${file_extension})
    fileName=$(gunzip_if_gzipped ${fileName})
    echo Beginning to run ${python_script}
    python3 $python_script $fileName
fi
rm $fileName
mv TCGA*${tcga_extension} ../
cd ../
if [ -d "InputData" ]
then
    mv TCGA*${tcga_extension} InputData/
else
    mkdir InputData
    mv TCGA*${tcga_extension} InputData/
fi

cd InputData/

for file in `ls -p | grep -v /`; do
    IFS='.' read -ra cancertype <<< "$file"
    mydir="${cancertype[0]}"
    if [ -d $mydir"/$folder/" ]
    then
        mv $file $mydir/$folder/
    else
        if [ -d $mydir ]
        then
            mkdir $mydir/$folder
            mv $file $mydir/$folder/
        else
            mkdir $mydir
            mkdir $mydir/$folder
            mv $file $mydir/$folder/
        fi
    fi
done

}

execulte_analysis() {
search_dir=Data_To_Process_Files
dockerCommandsFile=$1
for file in `ls $search_dir`; do
	IFS='.' read -ra Analysis <<< "$file"
	datafile=${search_dir}/${file}
	analysis="${Analysis[0]}"
	python3 create_temporary_bash_scripts.py $analysis $datafile
done
}

evaluate_results() {
experiment_name=$1
new_output=${experiment_name}"_metrics.tsv"
new_predictions=${experiment_name}"_Predictions.tsv.gz"
search_dir=Data_To_Process_Files
for file in `ls $search_dir`; do
    IFS='.' read -ra Analysis <<< "$file"
	datafile=${search_dir}/${file}
	analysis="${Analysis[0]}"
	IFS='_' read -ra trial <<< "$analysis"
    python3 get_metrics.py $analysis $datafile
    output=${analysis}".tsv"
	cd Analysis_Results
	if [[ "${trail[0]}" == "CNV" ]];
	then
	    cat $output >> $new_output
	else
	    tail -n +2 $output >> $new_output
	fi
	cd ../
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
}

set +a
