#!/usr/bin/env bash

fileName="mmc1.xlsx"
if [ -e $fileName* ]
then
    python3 Covariate.py $fileName
else
    echo $fileName has not yest been downloaded
    wget https://www.cell.com/cms/10.1016/j.cell.2018.02.052/attachment/f4eb6b31-8957-4817-a41f-e46fd2a1d9c3/${fileName}
    python3 Covariate.py $fileName
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

for file in `ls -p | grep -v /`; do
    IFS='.' read -ra cancertype <<< "$file"
    mydir="${cancertype[0]}"
    if [ -d $mydir"/Covariate/" ]
    then
        mv $file $mydir/Covariate/
    else
        if [ -d $mydir ]
        then
            mkdir $mydir/Covariate
            mv $file $mydir/Covariate/
        else
            mkdir $mydir
            mkdir $mydir/Covariate
            mv $file $mydir/Covariate/
        fi
    fi
done

cd ../
cd DataStandardization/
python3 Class.py
