#!/usr/bin/env bash
. ./functions.sh
tarFile="GSE62944_RAW"
fileName="GSM1536837_06_01_15_TCGA_24.tumor_Rsubread_TPM.txt"
extension2=".gz"
extention=".tar"
file_to_check="../InputData/TCGA_BRCA/Expression/*ttsv"
check_if_file_already_exits $file_to_check

compressedFile=${tarFile}${extention}

for file in `ls `; do
    if [[ $file == GSM* ]]
    then
        if [ $file == $fileName$extension2 ]
        then
            echo kept $file
        else
            if [ $file == $fileName ]
            then
                echo kept $file
            else
                echo removed $file
                rm $file
            fi
        fi
    fi
done

if [ -f $fileName ]
then
    python3 Expression.py $fileName
else
    if [ -f $fileName$extension2 ]
    then
        gunzip $fileName$extension2
        python3 Expression.py $fileName
    else
        if [ -f $tarFile ]
        then
            tar -xvf GSE62944_RAW.tar
            gunzip $fileName$extension2
            python3 Expression.py $fileName
            for file in `ls `; do
                if [[ $file == GSM* ]]
                then
                    if [ $file == $fileName$extension2 ]
                    then
                        echo kept $file
                    else
                        if [ $file == $fileName ]
                        then
                            echo kept $file
                        else
                            echo removed $file
                        fi
                    fi
                fi
            done
        else
            wget ftp://ftp.ncbi.nlm.nih.gov/geo/series/GSE62nnn/GSE62944/suppl/$compressedFile
            tar -xvf GSE62944_RAW.tar
            gunzip $fileName$extension2
            python3 Expression.py $fileName
            for file in `ls `; do
                if [[ $file == GSM* ]]
                then
                    if [ $file == $fileName$extension2 ]
                    then
                        echo kept $file
                    else
                        if [ $file == $fileName ]
                        then
                            echo kept $file
                        else
                            echo removed $file
                        fi
                    fi
                fi
            done
        fi
    fi
fi

mv TCGA*ttsv ../
cd ../

if [ -d "InputData" ]
then
    mv TCGA*\.ttsv InputData/
else
    mkdir InputData
    mv TCGA*\.ttsv InputData/
fi

cd InputData/
for file in `ls -p | grep -v /`; do
    IFS='.' read -ra cancertype <<< "$file"
    mydir="${cancertype[0]}"
    if [ -d $mydir"/Expression/" ]
    then
        mv $file $mydir/Expression/
    else
        if [ -d $mydir ]
        then
            mkdir $mydir/Expression
            mv $file $mydir/Expression/
        else
            mkdir $mydir
            mkdir $mydir/Expression
            mv $file $mydir/Expression/
        fi
    fi
done
