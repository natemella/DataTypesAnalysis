#!/usr/bin/env bash

#!/usr/bin/env bash

fileName="TCGA-RPPA-pancan-clean.xena"
extention=".gz"
unzippedFile=${fileName}${extention}

if [ -e $fileName* ]
then
    gunzip $unzippedFile
    echo IT WORKED!!!
    python RPPA.py $fileName
#    cat $fileName
else
    echo $unzippedFile has not yest been downloaded
    wget https://pancanatlas.xenahubs.net/download/${unzippedFile}
    bash RPPA.sh
fi
rm $fileName
mv *.tsv ../
cd ../
if [ -d "InputData" ]
then
    mv *.tsv InputData/
else
    mkdir InputData
    mv *.tsv InputData/
fi

cd InputData/

Path=$(pwd)
Files=${Path}/*

echo Path
echo $Files


if [ -d "TCGA_BLCA/RPPA/" ]
then
    mv TCGA_BLCA.tsv TCGA_BLCA/RPPA/
else
    if [ -d "TCGA_BLCA" ]
    then
        mkdir TCGA_BLCA/RPPA
        mv TCGA_BLCA.tsv TCGA_BLCA/RPPA/
    else
        mkdir TCGA_BLCA
        mkdir TCGA_BLCA/RPPA
        mv TCGA_BLCA.tsv TCGA_BLCA/RPPA/
    fi
fi
if [ -d "TCGA_COAD/RPPA/" ]
then
    mv TCGA_COAD.tsv TCGA_COAD/RPPA/
else
    if [ -d "TCGA_COAD" ]
    then
        mkdir TCGA_COAD/RPPA
        mv TCGA_COAD.tsv TCGA_COAD/RPPA/
    else
        mkdir TCGA_COAD
        mkdir TCGA_COAD/RPPA
        mv TCGA_COAD.tsv TCGA_COAD/RPPA/
    fi
fi
if [ -d "TCGA_GBM/RPPA/" ]
then
    mv TCGA_GBM.tsv TCGA_GBM/RPPA/
else
    if [ -d "TCGA_GBM" ]
    then
        mkdir TCGA_GBM/RPPA
        mv TCGA_GBM.tsv TCGA_GBM/RPPA/
    else
        mkdir TCGA_GBM
        mkdir TCGA_GBM/RPPA
        mv TCGA_GBM.tsv TCGA_GBM/RPPA/
    fi
fi
if [ -d "TCGA_KIRC/RPPA/" ]
then
    mv TCGA_KIRC.tsv TCGA_KIRC/RPPA/
else
    if [ -d "TCGA_KIRC/" ]
    then
        mkdir TCGA_KIRC/RPPA
        mv TCGA_KIRC.tsv TCGA_KIRC/RPPA/
    else
        mkdir TCGA_KIRC
        mkdir TCGA_KIRC/RPPA
        mv TCGA_KIRC.tsv TCGA_KIRC/RPPA/
    fi
fi
if [ -d "TCGA_LUAD/RPPA/" ]
then
    mv TCGA_LUAD.tsv TCGA_LUAD/RPPA/
else
    if [ -d "TCGA_LUAD" ]; then
        mkdir TCGA_LUAD/RPPA
        mv TCGA_LUAD.tsv TCGA_LUAD/RPPA/
    else
        mkdir TCGA_LUAD
        mkdir TCGA_LUAD/RPPA
        mv TCGA_LUAD.tsv TCGA_LUAD/RPPA/
    fi
fi
if [ -d "TCGA_PRAD/RPPA/" ]
then
    mv TCGA_PRAD.tsv TCGA_PRAD/RPPA/
else
    if [ -d "TCGA_PRAD" ]; then
        mkdir TCGA_PRAD/RPPA
        mv TCGA_PRAD.tsv TCGA_PRAD/RPPA/
    else
        mkdir TCGA_PRAD
        mkdir TCGA_PRAD/RPPA
        mv TCGA_PRAD.tsv TCGA_PRAD/RPPA/
    fi
fi
if [ -d "TCGA_SARC/RPPA/" ]
then
    mv TCGA_SARC.tsv TCGA_SARC/RPPA/
else
    if [ -d "TCGA_SARC/" ]; then
        mkdir TCGA_SARC/RPPA
        mv TCGA_SARC.tsv TCGA_SARC/RPPA/
    else
        mkdir TCGA_SARC
        mkdir TCGA_SARC/RPPA
        mv TCGA_SARC.tsv TCGA_SARC/RPPA/
    fi
fi
if [ -d "TCGA_OV/RPPA/" ]
then
    mv TCGA_OV.tsv TCGA_OV/RPPA/
else
    if [ -d "TCGA_OV/RPPA/" ]
    then
        mkdir TCGA_OV/RPPA
        mv TCGA_OV.tsv TCGA_OV/RPPA/
    else
        mkdir TCGA_OV
        mkdir TCGA_OV/RPPA
        mv TCGA_OV.tsv TCGA_OV/RPPA/
    fi
fi
if [ -d "TCGA_SKCM/RPPA/" ]
then
    mv TCGA_SKCM.tsv TCGA_SKCM/RPPA/
else
    if [ -d "TCGA_SKCM/" ]
    then
        mkdir TCGA_SKCM/RPPA
        mv TCGA_SKCM.tsv TCGA_SKCM/RPPA/
    else
        mkdir TCGA_SKCM
        mkdir TCGA_SKCM/RPPA
        mv TCGA_SKCM.tsv TCGA_SKCM/RPPA/
    fi
fi
if [ -d "TCGA_BRCA/RPPA/" ]
then
    mv TCGA_BRCA.tsv TCGA_BRCA/RPPA/
else
    if [ -d "TCGA_BRCA/" ]
    then
        mkdir TCGA_BRCA/RPPA
        mv TCGA_BRCA.tsv TCGA_BRCA/RPPA/
    else
        mkdir TCGA_BRCA
        mkdir TCGA_BRCA/RPPA
        mv TCGA_BRCA.tsv TCGA_BRCA/RPPA/
    fi
fi
if [ -d "TCGA_LUSC/RPPA/" ]
then
    mv TCGA_LUSC.tsv TCGA_LUSC/RPPA/
else
    if [ -d "TCGA_LUSC/" ]
    then
        mkdir TCGA_LUSC/RPPA
        mv TCGA_LUSC.tsv TCGA_LUSC/RPPA/
    else
        mkdir TCGA_LUSC
        mkdir TCGA_LUSC/RPPA
        mv TCGA_LUSC.tsv TCGA_LUSC/RPPA/
    fi
fi

