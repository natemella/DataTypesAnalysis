#!/usr/bin/env bash
set -a # export all functions
set -e

rename_if_necessary() {
fileName=$1
rename=$2
extension=$3
if [[ $rename == True ]];
then
    echo RENAMING FILE PRIOR TO PROCESSING
    mv $fileName ${fileName}${extension}
    echo ${fileName}
else
    echo ${fileName}
fi
}
gunzip_if_gzipped() {
fileName=$1
if [[ $fileName =~ \.gz$ ]];
then
    gunzip ${fileName}
    echo ${fileName}
else
    echo ${fileName}
fi
}

download_and_organize_data() {
fileName=$1
python_script=$2
web_url=$3
tcga_extension=$4
folder=$5
file_extension=$6
rename=$7

echo $rename

if [ -e $fileName* ]
then
    fileName=$(rename_if_necessary ${fileName} ${rename} ${file_extension})
    fileName=$(gunzip_if_gzipped ${fileName})
    python3 $python_script $fileName
    echo ${fileName}
else
    echo $fileName has not yest been downloaded
    wget ${web_url}/${fileName}
    fileName=$(rename_if_necessary ${fileName} ${rename} ${file_extension})
    fileName=$(gunzip_if_gzipped ${fileName})
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
