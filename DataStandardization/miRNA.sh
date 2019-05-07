#!/usr/bin/env bash

fileName="pancanMiRs_EBadjOnProtocolPlatformWithoutRepsWithUnCorrectMiRs_08_04_16.xena"
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

echo Path
echo $Files


if [ -d "TCGA_BLCA/miRNA/" ]
then
    mv TCGA_BLCA.ttsv TCGA_BLCA/miRNA/
else
    if [ -d "TCGA_BLCA" ]
    then
        mkdir TCGA_BLCA/miRNA
        mv TCGA_BLCA.ttsv TCGA_BLCA/miRNA/
    else
        mkdir TCGA_BLCA
        mkdir TCGA_BLCA/miRNA
        mv TCGA_BLCA.ttsv TCGA_BLCA/miRNA/
    fi
fi
if [ -d "TCGA_COAD/miRNA/" ]
then
    mv TCGA_COAD.ttsv TCGA_COAD/miRNA/
else
    if [ -d "TCGA_COAD" ]
    then
        mkdir TCGA_COAD/miRNA
        mv TCGA_COAD.ttsv TCGA_COAD/miRNA/
    else
        mkdir TCGA_COAD
        mkdir TCGA_COAD/miRNA
        mv TCGA_COAD.ttsv TCGA_COAD/miRNA/
    fi
fi
if [ -d "TCGA_GBM/miRNA/" ]
then
    mv TCGA_GBM.ttsv TCGA_GBM/miRNA/
else
    if [ -d "TCGA_GBM" ]
    then
        mkdir TCGA_GBM/miRNA
        mv TCGA_GBM.ttsv TCGA_GBM/miRNA/
    else
        mkdir TCGA_GBM
        mkdir TCGA_GBM/miRNA
        mv TCGA_GBM.ttsv TCGA_GBM/miRNA/
    fi
fi
if [ -d "TCGA_KIRC/miRNA/" ]
then
    mv TCGA_KIRC.ttsv TCGA_KIRC/miRNA/
else
    if [ -d "TCGA_KIRC/" ]
    then
        mkdir TCGA_KIRC/miRNA
        mv TCGA_KIRC.ttsv TCGA_KIRC/miRNA/
    else
        mkdir TCGA_KIRC
        mkdir TCGA_KIRC/miRNA
        mv TCGA_KIRC.ttsv TCGA_KIRC/miRNA/
    fi
fi
if [ -d "TCGA_LUAD/miRNA/" ]
then
    mv TCGA_LUAD.ttsv TCGA_LUAD/miRNA/
else
    if [ -d "TCGA_LUAD" ]; then
        mkdir TCGA_LUAD/miRNA
        mv TCGA_LUAD.ttsv TCGA_LUAD/miRNA/
    else
        mkdir TCGA_LUAD
        mkdir TCGA_LUAD/miRNA
        mv TCGA_LUAD.ttsv TCGA_LUAD/miRNA/
    fi
fi
if [ -d "TCGA_PRAD/miRNA/" ]
then
    mv TCGA_PRAD.ttsv TCGA_PRAD/miRNA/
else
    if [ -d "TCGA_PRAD" ]; then
        mkdir TCGA_PRAD/miRNA
        mv TCGA_PRAD.ttsv TCGA_PRAD/miRNA/
    else
        mkdir TCGA_PRAD
        mkdir TCGA_PRAD/miRNA
        mv TCGA_PRAD.ttsv TCGA_PRAD/miRNA/
    fi
fi
if [ -d "TCGA_SARC/miRNA/" ]
then
    mv TCGA_SARC.ttsv TCGA_SARC/miRNA/
else
    if [ -d "TCGA_SARC/" ]; then
        mkdir TCGA_SARC/miRNA
        mv TCGA_SARC.ttsv TCGA_SARC/miRNA/
    else
        mkdir TCGA_SARC
        mkdir TCGA_SARC/miRNA
        mv TCGA_SARC.ttsv TCGA_SARC/miRNA/
    fi
fi
if [ -d "TCGA_OV/miRNA/" ]
then
    mv TCGA_OV.ttsv TCGA_OV/miRNA/
else
    if [ -d "TCGA_OV/miRNA/" ]
    then
        mkdir TCGA_OV/miRNA
        mv TCGA_OV.ttsv TCGA_OV/miRNA/
    else
        mkdir TCGA_OV
        mkdir TCGA_OV/miRNA
        mv TCGA_OV.ttsv TCGA_OV/miRNA/
    fi
fi
if [ -d "TCGA_SKCM/miRNA/" ]
then
    mv TCGA_SKCM.ttsv TCGA_SKCM/miRNA/
else
    if [ -d "TCGA_SKCM/" ]
    then
        mkdir TCGA_SKCM/miRNA
        mv TCGA_SKCM.ttsv TCGA_SKCM/miRNA/
    else
        mkdir TCGA_SKCM
        mkdir TCGA_SKCM/miRNA
        mv TCGA_SKCM.ttsv TCGA_SKCM/miRNA/
    fi
fi
if [ -d "TCGA_BRCA/miRNA/" ]
then
    mv TCGA_BRCA.ttsv TCGA_BRCA/miRNA/
else
    if [ -d "TCGA_BRCA/" ]
    then
        mkdir TCGA_BRCA/miRNA
        mv TCGA_BRCA.ttsv TCGA_BRCA/miRNA/
    else
        mkdir TCGA_BRCA
        mkdir TCGA_BRCA/miRNA
        mv TCGA_BRCA.ttsv TCGA_BRCA/miRNA/
    fi
fi
if [ -d "TCGA_LUSC/miRNA/" ]
then
    mv TCGA_LUSC.ttsv TCGA_LUSC/miRNA/
else
    if [ -d "TCGA_LUSC/" ]
    then
        mkdir TCGA_LUSC/miRNA
        mv TCGA_LUSC.ttsv TCGA_LUSC/miRNA/
    else
        mkdir TCGA_LUSC
        mkdir TCGA_LUSC/miRNA
        mv TCGA_LUSC.ttsv TCGA_LUSC/miRNA/
    fi
fi

