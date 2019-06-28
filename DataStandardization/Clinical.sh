#!/usr/bin/env bash
. ./functions.sh
fileName="GSE62944_06_01_15_TCGA_24_548_Clinical_Variables_9264_Samples.txt.gz"
web_url="ftp://ftp.ncbi.nlm.nih.gov/geo/series/GSE62nnn/GSE62944/suppl/"
python_script=Clinical.py
folder="Clinical"
tcga_extension=".tsv"
force=$1
echo $force
download_and_organize_data $fileName $python_script $web_url $tcga_extension $folder $force
cd ../../

for c in `python3 DataTypesAnalysis/DataStandardization/get_clinical_paths.py`; do
    gzip $c
    Rscript --vanilla scripts/Impute.R $c".gz" true
    python3 scripts/Scale.py $c".gz" true robust
    gunzip $c".gz"
done

python3 DataTypesAnalysis/DataStandardization/Clinical_After_Scaling.py

for c in `python3 DataTypesAnalysis/DataStandardization/get_clinical_paths.py`; do
    gzip $c
    python3 scripts/OneHotEncode.py $c".gz"
    gunzip $c".gz"
done
