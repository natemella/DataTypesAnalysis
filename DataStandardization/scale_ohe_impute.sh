#!/usr/bin/env bash
. ./functions.sh

set -e

scaling() {
filename=$1
cd ../
python3 scripts/Scale.py DataTypesAnalysis/InputData${filename} true robust
cd DataTypesAnalysis/
}

imputing() {
filename=$1
cd ../
pwd
Rscript --vanilla scripts/Impute.R DataTypesAnalysis/InputData${filename} true
cd DataTypesAnalysis/
}

one-hot_encoding() {
filename=$1
cd ../
python3 scripts/OneHotEncode.py DataTypesAnalysis/InputData${filename}
cd DataTypesAnalysis/
}

get_extension() {
filename=$1
IFS='.' read -ra mylist <<< "$filename"
extension="${mylist[1]}"
echo $extension
}

cd ..
for c in `python3 DataStandardization/get_cut_paths.py`; do
    gunzip_if_gzipped InputData$c
done
for c in `python3 DataStandardization/get_cut_paths.py`; do
    echo gzipping $c
    gzip -f InputData$c
done
for c in `python3 DataStandardization/get_cut_paths.py`; do
    echo imputing $c
    imputing $c
done
for c in `python3 DataStandardization/get_cut_paths.py`; do
    echo one-hot_encoding $c
    one-hot_encoding $c
done
for c in `python3 DataStandardization/get_cut_paths.py`; do
    IFS="/" read -ra mylist <<< "InputData$c"
    data_type="${mylist[2]}"
    if [[ $data_type =~ ^(Covariate|Expression|RPPA|miRNA)$ ]]; then
        echo scaling ${c}
        scaling 'InputData'$c
    fi
done

