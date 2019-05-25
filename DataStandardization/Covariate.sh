#!/usr/bin/env bash

fileName="mmc1.xlsx"
extension=".CSV"
if [ -e $fileName* ]
then
    echo IT WORKED!!!
    mkdir xls/
    mv mmc1.xlsx mmc1.xls
    mv $fileName xls/
    mkdir csv/
    docker run -v `pwd`xls:/src -it mrooding/docker-ssconvert-xls2csv
    echo IT WORKED!!!
#    python3 Covariate.py $fileName
#    cat $fileName
else
    echo $fileName has not yest been downloaded
    wget https://www.cell.com/cms/10.1016/j.cell.2018.02.052/attachment/f4eb6b31-8957-4817-a41f-e46fd2a1d9c3/${fileName}
    mv $fileName mmc1.xls
    mkdir /sir/xls/
    mv $fileName /sir/xls/
    mkdir csv/
    docker run -v `pwd`xls:/src -it mrooding/docker-ssconvert-xls2csv
    echo IT WORKED!!!
#    python3 Covariate.py $fileName
fi
#rm $fileName
#rm $fileName$extension
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
#for file in `ls `; do
#    IFS='.' read -ra cancertype <<< "$file"
#    mydir="${cancertype[0]}"
#    if [ -d $mydir"/Covariate/" ]
#    then
#        mv $mydir".tsv" $mydir/Covariate/
#    else
#        if [ -d $mydir ]
#        then
#            mkdir $mydir/Covariate
#            mv $mydir".tsv" $mydir/Covariate/
#        else
#            mkdir $mydir
#            mkdir $mydir/Covariate
#            mv $mydir".tsv" $mydir/Covariate/
#        fi
#    fi
#done
#
#cd ../
#cd DataStandardization/
#python3 Class.py
#rm summary.txt
##rm result.tsv
##rm cancer_test.csv