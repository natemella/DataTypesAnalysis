#!/usr/bin/env bash

fileName="1c8cfe5f-e52d-41ba-94da-f15ea1337efc"
extention=".gz"
unzippedFile=${fileName}${extention}

if [ -e $fileName* ]
then
    mv $fileName $unzippedFile
    gunzip $unzippedFile
    mv $unzippedFile $fileName
    echo IT WORKED!!!
    python3 SM.py
#    cat $fileName
else
    echo $fileName has not yest been downloaded
    wget https://api.gdc.cancer.gov/data/${fileName}
    bash SM.sh
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
for file in `ls `; do
    IFS='.' read -ra cancertype <<< "$file"
    mydir="${cancertype[0]}"
    if [ -d $mydir"/SM/" ]
    then
        mv $mydir".tsv" $mydir/SM/
    else
        if [ -d $mydir ]
        then
            mkdir $mydir/SM
            mv $mydir".tsv" $mydir/SM/
        else
            mkdir $mydir
            mkdir $mydir/SM
            mv $mydir".tsv" $mydir/SM/
        fi
    fi
done

