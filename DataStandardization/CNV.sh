#!/usr/bin/env bash

fileName="broad.mit.edu_PANCAN_Genome_Wide_SNP_6_whitelisted.gene.xena"
extention=".gz"
unzippedFile=${fileName}${extention}

if [ -e $fileName* ]
then
    gunzip $unzippedFile
    echo IT WORKED!!!
    python3 miRNA.py $fileName
#    cat $fileName
else
    echo $unzippedFile has not yest been downloaded
    wget https://pancanatlas.xenahubs.net/download/${unzippedFile}
    gunzip $unzippedFile
    echo IT WORKED!!!
    python3 miRNA.py $fileName
fi
rm $fileName
mv *.ttsv ../
cd ../
if [ -d "InputData" ]
then
    mv *.ttsv InputData/
else
    mkdir InputData
    mv *.ttsv InputData/
fi

cd InputData/


for file in `ls -p | grep -v /`; do
    IFS='.' read -ra cancertype <<< "$file"
    mydir="${cancertype[0]}"
    if [ -d $mydir"/CNV/" ]
    then
        mv $file $mydir/CNV/
    else
        if [ -d $mydir ]
        then
            mkdir $mydir/CNV
            mv $file $mydir/CNV/
        else
            mkdir $mydir
            mkdir $mydir/CNV
            mv $file $mydir/CNV/
        fi
    fi
done



