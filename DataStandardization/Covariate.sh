#!/usr/bin/env bash

fileName="TCGA-RPPA-pancan-clean.xena"

if [ -e $fileName* ]
then
    echo IT WORKED!!!
    python3 Covariate.py $fileName
#    cat $fileName
else
    echo $fileName has not yest been downloaded
    wget https://pancanatlas.xenahubs.net/download/${fileName}
    bash RPPA.sh
fi
rm $fileName
mv TCGA*.tsv ../
cd ../
if [ -d "InputData" ]
then
    mv TCGA*.tsv InputData/
else
    mkdir InputData
    mv TCGA*.tsv InputData/
fi

cd InputData/

Path=$(pwd)
Files=${Path}/*

for file in `ls `; do
    IFS='.' read -ra cancertype <<< "$file"
    mydir="${cancertype[0]}"
    if [ -d $mydir"/RPPA/" ]
    then
        mv $mydir".tsv" $mydir/RPPA/
    else
        if [ -d $mydir ]
        then
            mkdir $mydir/RPPA
            mv $mydir".tsv" $mydir/RPPA/
        else
            mkdir $mydir
            mkdir $mydir/RPPA
            mv $mydir".tsv" $mydir/RPPA/
        fi
    fi
done