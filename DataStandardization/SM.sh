#!/usr/bin/env bash

#!/usr/bin/env bash

#!/usr/bin/env bash

fileName="1c8cfe5f-e52d-41ba-94da-f15ea1337efc"
extention=".gz"
unzippedFile=${fileName}${extention}

if [ -e $fileName* ]
then
    mv $fileName $unzippedFile
    gunzip $unzippedFile
    echo IT WORKED!!!
    python3 SM.py $fileName
#    cat $fileName
else
    echo $fileName has not yest been downloaded
    wget https://api.gdc.cancer.gov/data/${fileName}
    bash SM.sh
fi
#rm $fileName
#mv TCGA*.tsv ../
cd ../
for file in `ls `; do
    IFS='.' read -ra cancertype <<< "$file"
    echo "${cancertype[0]}"
done
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
#echo Path
#echo $Files
#
#
#if [ -d "TCGA_BLCA/SM/" ]
#then
#    mv TCGA_BLCA.tsv TCGA_BLCA/SM/
#else
#    if [ -d "TCGA_BLCA" ]
#    then
#        mkdir TCGA_BLCA/SM
#        mv TCGA_BLCA.tsv TCGA_BLCA/SM/
#    else
#        mkdir TCGA_BLCA
#        mkdir TCGA_BLCA/SM
#        mv TCGA_BLCA.tsv TCGA_BLCA/SM/
#    fi
#fi
#if [ -d "TCGA_COAD/SM/" ]
#then
#    mv TCGA_COAD.tsv TCGA_COAD/SM/
#else
#    if [ -d "TCGA_COAD" ]
#    then
#        mkdir TCGA_COAD/SM
#        mv TCGA_COAD.tsv TCGA_COAD/SM/
#    else
#        mkdir TCGA_COAD
#        mkdir TCGA_COAD/SM
#        mv TCGA_COAD.tsv TCGA_COAD/SM/
#    fi
#fi
#if [ -d "TCGA_GBM/SM/" ]
#then
#    mv TCGA_GBM.tsv TCGA_GBM/SM/
#else
#    if [ -d "TCGA_GBM" ]
#    then
#        mkdir TCGA_GBM/SM
#        mv TCGA_GBM.tsv TCGA_GBM/SM/
#    else
#        mkdir TCGA_GBM
#        mkdir TCGA_GBM/SM
#        mv TCGA_GBM.tsv TCGA_GBM/SM/
#    fi
#fi
#if [ -d "TCGA_KIRC/SM/" ]
#then
#    mv TCGA_KIRC.tsv TCGA_KIRC/SM/
#else
#    if [ -d "TCGA_KIRC/" ]
#    then
#        mkdir TCGA_KIRC/SM
#        mv TCGA_KIRC.tsv TCGA_KIRC/SM/
#    else
#        mkdir TCGA_KIRC
#        mkdir TCGA_KIRC/SM
#        mv TCGA_KIRC.tsv TCGA_KIRC/SM/
#    fi
#fi
#if [ -d "TCGA_LUAD/SM/" ]
#then
#    mv TCGA_LUAD.tsv TCGA_LUAD/SM/
#else
#    if [ -d "TCGA_LUAD" ]; then
#        mkdir TCGA_LUAD/SM
#        mv TCGA_LUAD.tsv TCGA_LUAD/SM/
#    else
#        mkdir TCGA_LUAD
#        mkdir TCGA_LUAD/SM
#        mv TCGA_LUAD.tsv TCGA_LUAD/SM/
#    fi
#fi
#if [ -d "TCGA_PRAD/SM/" ]
#then
#    mv TCGA_PRAD.tsv TCGA_PRAD/SM/
#else
#    if [ -d "TCGA_PRAD" ]; then
#        mkdir TCGA_PRAD/SM
#        mv TCGA_PRAD.tsv TCGA_PRAD/SM/
#    else
#        mkdir TCGA_PRAD
#        mkdir TCGA_PRAD/SM
#        mv TCGA_PRAD.tsv TCGA_PRAD/SM/
#    fi
#fi
#if [ -d "TCGA_SARC/SM/" ]
#then
#    mv TCGA_SARC.tsv TCGA_SARC/SM/
#else
#    if [ -d "TCGA_SARC/" ]; then
#        mkdir TCGA_SARC/SM
#        mv TCGA_SARC.tsv TCGA_SARC/SM/
#    else
#        mkdir TCGA_SARC
#        mkdir TCGA_SARC/SM
#        mv TCGA_SARC.tsv TCGA_SARC/SM/
#    fi
#fi
#if [ -d "TCGA_OV/SM/" ]
#then
#    mv TCGA_OV.tsv TCGA_OV/SM/
#else
#    if [ -d "TCGA_OV/SM/" ]
#    then
#        mkdir TCGA_OV/SM
#        mv TCGA_OV.tsv TCGA_OV/SM/
#    else
#        mkdir TCGA_OV
#        mkdir TCGA_OV/SM
#        mv TCGA_OV.tsv TCGA_OV/SM/
#    fi
#fi
#if [ -d "TCGA_SKCM/SM/" ]
#then
#    mv TCGA_SKCM.tsv TCGA_SKCM/SM/
#else
#    if [ -d "TCGA_SKCM/" ]
#    then
#        mkdir TCGA_SKCM/SM
#        mv TCGA_SKCM.tsv TCGA_SKCM/SM/
#    else
#        mkdir TCGA_SKCM
#        mkdir TCGA_SKCM/SM
#        mv TCGA_SKCM.tsv TCGA_SKCM/SM/
#    fi
#fi
#if [ -d "TCGA_BRCA/SM/" ]
#then
#    mv TCGA_BRCA.tsv TCGA_BRCA/SM/
#else
#    if [ -d "TCGA_BRCA/" ]
#    then
#        mkdir TCGA_BRCA/SM
#        mv TCGA_BRCA.tsv TCGA_BRCA/SM/
#    else
#        mkdir TCGA_BRCA
#        mkdir TCGA_BRCA/SM
#        mv TCGA_BRCA.tsv TCGA_BRCA/SM/
#    fi
#fi
#if [ -d "TCGA_LUSC/SM/" ]
#then
#    mv TCGA_LUSC.tsv TCGA_LUSC/SM/
#else
#    if [ -d "TCGA_LUSC/" ]
#    then
#        mkdir TCGA_LUSC/SM
#        mv TCGA_LUSC.tsv TCGA_LUSC/SM/
#    else
#        mkdir TCGA_LUSC
#        mkdir TCGA_LUSC/SM
#        mv TCGA_LUSC.tsv TCGA_LUSC/SM/
#    fi
#fi
