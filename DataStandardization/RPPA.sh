#!/usr/bin/env bash

set -e
. ./functions.sh
fileName="TCGA-RPPA-pancan-clean.xena.gz"
python_script=RPPA.py
web_url="https://pancanatlas.xenahubs.net/download"
tcga_extension=".tsv"
folder=RPPA

download_and_organize_data $fileName $python_script $web_url $tcga_extension $folder

fileName="TCGA-RPPA-pancan-clean.xena"

#if [ -e $fileName* ]
#then
#    gunzip $unzippedFile
#    echo IT WORKED!!!
#    python3 RPPA.py $fileName
##    cat $fileName
#else
#    echo $unzippedFile has not yest been downloaded
#    wget https://pancanatlas.xenahubs.net/download/${unzippedFile}
#    bash RPPA.sh
#fi
#rm $fileName
#mv TCGA*.tsv ../
#cd ../
#if [ -d "InputData" ]
#then
#    mv TCGA*.tsv InputData/
#else
#    mkdir InputData
#    mv TCGA*.tsv InputData/
#fi
#
#cd InputData/
#
#Path=$(pwd)
#Files=${Path}/*
#
#for file in `ls -p | grep -v /`; do
#    IFS='.' read -ra cancertype <<< "$file"
#    mydir="${cancertype[0]}"
#    if [ -d $mydir"/RPPA/" ]
#    then
#        mv $file $mydir/RPPA/
#    else
#        if [ -d $mydir ]
#        then
#            mkdir $mydir/RPPA
#            mv $file $mydir/RPPA/
#        else
#            mkdir $mydir
#            mkdir $mydir/RPPA
#            mv $file $mydir/RPPA/
#        fi
#    fi
#done
