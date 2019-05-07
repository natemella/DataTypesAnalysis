#!/usr/bin/env bash

fileName="pancanMiRs_EBadjOnProtocolPlatformWithoutRepsWithUnCorrectMiRs_08_04_16.xena"
extention=".gz"
unzippedFile=${fileName}${extention}

if [ -f $fileName* ]
then
    gunzip $unzippedFile
    echo IT WORKED!!!
    python miRNA.py $fileName
#    cat $fileName
else
    echo $unzippedFile has not yest been downloaded
    wget https://pancanatlas.xenahubs.net/download/${unzippedFile}
    bash miRNA.sh
fi



