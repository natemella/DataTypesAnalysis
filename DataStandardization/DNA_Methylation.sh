#!/usr/bin/env bash
. ./functions.sh
file="GPL16304-47833.txt.gz"
set -e
file_to_check="../InputData/TCGA_BRCA/DNA_Methylation/*.tsv"
check_if_file_already_exits $file_to_check
if [ -e $file ]
then
	for c in `cat CancerTypes.txt`; do
	    Rscript DNA_Methylation.R "https://tcga.xenahubs.net/download/TCGA."$c".sampleMap/HumanMethylation450.gz" "TCGA_"$c".tsv";
	done;
else
	wget "https://www.dropbox.com/s/8m7ourb5ucyvcf6/GPL16304-47833.txt.gz?dl=0&file_subpath=%2FGPL16304-47833.txt"
	mv 'GPL16304-47833.txt.gz?dl=0&file_subpath=%2FGPL16304-47833.txt' $file
	for c in `cat CancerTypes.txt`; do
	    Rscript DNA_Methylation.R "https://tcga.xenahubs.net/download/TCGA."$c".sampleMap/HumanMethylation450.gz" "TCGA_"$c".tsv";
	done;
fi
rm $file
mv TCGA*.tsv ../
cd ../
if [ -d "InputData" ]
then
    mv TCGA*.tsv InputData/
else
    mkdir InputData
    mv TCGA*.tsv InputData/
fi
cd InputData
for file in `ls -p | grep -v /`; do
    IFS='.' read -ra cancertype <<< "$file"
    mydir="${cancertype[0]}"
    if [ -d $mydir"/DNA_Methylation/" ]
    then
            mv $file $mydir/DNA_Methylation/
    else
        if [ -d $mydir ]
        then
            mkdir $mydir/DNA_Methylation
            mv $file $mydir/DNA_Methylation/
        else
            mkdir $mydir
            mkdir $mydir/DNA_Methylation
            mv $file $mydir/DNA_Methylation/
        fi
    fi
done
