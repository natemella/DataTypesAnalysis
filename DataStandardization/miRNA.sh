#!/usr/bin/env bash
set -e
. ./functions.sh
fileName="pancanMiRs_EBadjOnProtocolPlatformWithoutRepsWithUnCorrectMiRs_08_04_16.xena"
python_script=SM.py
web_url="https://api.gdc.cancer.gov/data/"
tcga_extension=".ttsv"
folder=miRNA
file_extension=".gz"
rename="True"
unzippedFile=${fileName}${file_extension}

download_and_organize_data $fileName $python_script $web_url $tcga_extension $folder $file_extension $rename

#
#if [ -e $fileName* ]
#then
#    gunzip $unzippedFile
#    echo IT WORKED!!!
#    python3 miRNA.py $fileName
##    cat $fileName
#else
#    echo $unzippedFile has not yest been downloaded
#    wget https://pancanatlas.xenahubs.net/download/${unzippedFile}
#    bash miRNA.sh
#fi
##rm $fileName
#mv *.ttsv ../
#cd ../
#if [ -d "InputData" ]
#then
#    mv *.ttsv InputData/
#else
#    mkdir InputData
#    mv *.ttsv InputData/
#fi
#
#cd InputData/
#
#Path=$(pwd)
#Files=${Path}/*
#
#
#for file in `ls -p | grep -v /`; do
#    IFS='.' read -ra cancertype <<< "$file"
#    mydir="${cancertype[0]}"
#    if [ -d $mydir"/miRNA/" ]
#    then
#        mv $file $mydir/miRNA/
#    else
#        if [ -d $mydir ]
#        then
#            mkdir $mydir/miRNA
#            mv $file $mydir/miRNA/
#        else
#            mkdir $mydir
#            mkdir $mydir/miRNA
#            mv $file $mydir/miRNA/
#        fi
#    fi
#done

