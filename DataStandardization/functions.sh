#!/usr/bin/env bash
set -a # export all functions

somefunc() {
fileName=$1
python_script=$2
web_url=$3
tcga_extension=$4
folder=$5
file_extension=$6

if [[ $fileName =~ \.gz$ ]];
then
    gunzip $fileName
fi

if [ -e $fileName* ]
then
    python3 $python_script $fileName
else
    echo $fileName has not yest been downloaded
    wget ${web_url}/${fileName}
    python3 $python_script $fileName
fi
rm $fileName
mv TCGA*${tcga_extension} ../
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
    if [ -d $mydir"/$folder/" ]
    then
        mv $file $mydir/$folder/
    else
        if [ -d $mydir ]
        then
            mkdir $mydir/$folder
            mv $file $mydir/$folder/
        else
            mkdir $mydir
            mkdir $mydir/$folder
            mv $file $mydir/$folder/
        fi
    fi
done

}

set +a
