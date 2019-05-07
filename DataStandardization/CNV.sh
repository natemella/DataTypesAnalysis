#!/usr/bin/env bash

fileName="broad.mit.edu_PANCAN_Genome_Wide_SNP_6_whitelisted.gene.xena"
extention=".gz"
unzippedFile=${fileName}${extention}

if [ -e $fileName* ]
then
    gunzip $unzippedFile
    echo IT WORKED!!!
    python miRNA.py $fileName
#    cat $fileName
else
    echo $unzippedFile has not yest been downloaded
    wget https://pancanatlas.xenahubs.net/download/${unzippedFile}
    bash CNV.sh
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

echo Path
echo $Files


if [ -d "TCGA_BLCA/CNV/" ]
then
    mv TCGA_BLCA.ttsv TCGA_BLCA/CNV/
else
    if [ -d "TCGA_BLCA" ]
    then
        mkdir TCGA_BLCA/CNV
        mv TCGA_BLCA.ttsv TCGA_BLCA/CNV/
    else
        mkdir TCGA_BLCA
        mkdir TCGA_BLCA/CNV
        mv TCGA_BLCA.ttsv TCGA_BLCA/CNV/
    fi
fi
if [ -d "TCGA_COAD/CNV/" ]
then
    mv TCGA_COAD.ttsv TCGA_COAD/CNV/
else
    if [ -d "TCGA_COAD" ]
    then
        mkdir TCGA_COAD/CNV
        mv TCGA_COAD.ttsv TCGA_COAD/CNV/
    else
        mkdir TCGA_COAD
        mkdir TCGA_COAD/CNV
        mv TCGA_COAD.ttsv TCGA_COAD/CNV/
    fi
fi
if [ -d "TCGA_GBM/CNV/" ]
then
    mv TCGA_GBM.ttsv TCGA_GBM/CNV/
else
    if [ -d "TCGA_GBM" ]
    then
        mkdir TCGA_GBM/CNV
        mv TCGA_GBM.ttsv TCGA_GBM/CNV/
    else
        mkdir TCGA_GBM
        mkdir TCGA_GBM/CNV
        mv TCGA_GBM.ttsv TCGA_GBM/CNV/
    fi
fi
if [ -d "TCGA_KIRC/CNV/" ]
then
    mv TCGA_KIRC.ttsv TCGA_KIRC/CNV/
else
    if [ -d "TCGA_KIRC/" ]
    then
        mkdir TCGA_KIRC/CNV
        mv TCGA_KIRC.ttsv TCGA_KIRC/CNV/
    else
        mkdir TCGA_KIRC
        mkdir TCGA_KIRC/CNV
        mv TCGA_KIRC.ttsv TCGA_KIRC/CNV/
    fi
fi
if [ -d "TCGA_LUAD/CNV/" ]
then
    mv TCGA_LUAD.ttsv TCGA_LUAD/CNV/
else
    if [ -d "TCGA_LUAD" ]; then
        mkdir TCGA_LUAD/CNV
        mv TCGA_LUAD.ttsv TCGA_LUAD/CNV/
    else
        mkdir TCGA_LUAD
        mkdir TCGA_LUAD/CNV
        mv TCGA_LUAD.ttsv TCGA_LUAD/CNV/
    fi
fi
if [ -d "TCGA_PRAD/CNV/" ]
then
    mv TCGA_PRAD.ttsv TCGA_PRAD/CNV/
else
    if [ -d "TCGA_PRAD" ]; then
        mkdir TCGA_PRAD/CNV
        mv TCGA_PRAD.ttsv TCGA_PRAD/CNV/
    else
        mkdir TCGA_PRAD
        mkdir TCGA_PRAD/CNV
        mv TCGA_PRAD.ttsv TCGA_PRAD/CNV/
    fi
fi
if [ -d "TCGA_SARC/CNV/" ]
then
    mv TCGA_SARC.ttsv TCGA_SARC/CNV/
else
    if [ -d "TCGA_SARC/" ]; then
        mkdir TCGA_SARC/CNV
        mv TCGA_SARC.ttsv TCGA_SARC/CNV/
    else
        mkdir TCGA_SARC
        mkdir TCGA_SARC/CNV
        mv TCGA_SARC.ttsv TCGA_SARC/CNV/
    fi
fi
if [ -d "TCGA_OV/CNV/" ]
then
    mv TCGA_OV.ttsv TCGA_OV/CNV/
else
    if [ -d "TCGA_OV/CNV/" ]
    then
        mkdir TCGA_OV/CNV
        mv TCGA_OV.ttsv TCGA_OV/CNV/
    else
        mkdir TCGA_OV
        mkdir TCGA_OV/CNV
        mv TCGA_OV.ttsv TCGA_OV/CNV/
    fi
fi
if [ -d "TCGA_SKCM/CNV/" ]
then
    mv TCGA_SKCM.ttsv TCGA_SKCM/CNV/
else
    if [ -d "TCGA_SKCM/" ]
    then
        mkdir TCGA_SKCM/CNV
        mv TCGA_SKCM.ttsv TCGA_SKCM/CNV/
    else
        mkdir TCGA_SKCM
        mkdir TCGA_SKCM/CNV
        mv TCGA_SKCM.ttsv TCGA_SKCM/CNV/
    fi
fi
if [ -d "TCGA_BRCA/CNV/" ]
then
    mv TCGA_BRCA.ttsv TCGA_BRCA/CNV/
else
    if [ -d "TCGA_BRCA/" ]
    then
        mkdir TCGA_BRCA/CNV
        mv TCGA_BRCA.ttsv TCGA_BRCA/CNV/
    else
        mkdir TCGA_BRCA
        mkdir TCGA_BRCA/CNV
        mv TCGA_BRCA.ttsv TCGA_BRCA/CNV/
    fi
fi
if [ -d "TCGA_LUSC/CNV/" ]
then
    mv TCGA_LUSC.ttsv TCGA_LUSC/CNV/
else
    if [ -d "TCGA_LUSC/" ]
    then
        mkdir TCGA_LUSC/CNV
        mv TCGA_LUSC.ttsv TCGA_LUSC/CNV/
    else
        mkdir TCGA_LUSC
        mkdir TCGA_LUSC/CNV
        mv TCGA_LUSC.ttsv TCGA_LUSC/CNV/
    fi
fi

