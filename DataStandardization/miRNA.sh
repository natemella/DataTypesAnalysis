#!/usr/bin/env bash

fileName="pancanMiRs_EBadjOnProtocolPlatformWithoutRepsWithUnCorrectMiRs_08_04_16.xena"
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
    bash miRNA.sh
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

Path=$(pwd)
Files=${Path}/*


for file in `ls `; do
    IFS='.' read -ra cancertype <<< "$file"
    mydir="${cancertype[0]}"
    if [ -d $mydir"/miRNA/" ]
    then
        mv $mydir".ttsv" $mydir/miRNA/
    else
        if [ -d $mydir ]
        then
            mkdir $mydir/miRNA
            mv $mydir".ttsv" $mydir/miRNA/
        else
            mkdir $mydir
            mkdir $mydir/miRNA
            mv $mydir".ttsv" $mydir/miRNA/
        fi
    fi
done

