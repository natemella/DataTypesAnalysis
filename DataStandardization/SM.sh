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
else
    echo $fileName has not yest been downloaded
    wget https://api.gdc.cancer.gov/data/${fileName}
    mv $fileName $unzippedFile
    gunzip $unzippedFile
    mv $unzippedFile $fileName
    echo IT WORKED!!!
    python3 SM.py
fi
if [ -e TCGA*.tsv ]
then
    rm $fileName
fi
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
for file in `ls -p | grep -v /`; do
    IFS='.' read -ra cancertype <<< "$file"
    mydir="${cancertype[0]}"
    if [ -d $mydir"/SM/" ]
    then
        mv $file $mydir/SM/
    else
        if [ -d $mydir ]
        then
            mkdir $mydir/SM
            mv $file $mydir/SM/
        else
            mkdir $mydir
            mkdir $mydir/SM
            mv $file $mydir/SM/
        fi
    fi
done
