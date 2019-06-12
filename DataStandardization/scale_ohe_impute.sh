#!/usr/bin/env bash
. ./functions.sh
set -e
scaling() {
filename=$1
docker run --rm -i \
  -v `pwd`"/InputData":"/InputData" \
  srp33/shinylearner:version515 \
    python3 /scripts/Scale.py /InputData${filename} true robust

}

imputing() {
filename=$1
echo $path
docker run --rm -i \
  -v `pwd`"/InputData":"/InputData" \
  srp33/shinylearner:version515 \
    Rscript --vanilla /scripts/Impute.R /InputData${filename} true

}

one-hot_encoding() {
filename=$1
docker run --rm -i \
  -v `pwd`"/InputData":"/InputData" \
  srp33/shinylearner:version515 \
    python3 /scripts/OneHotEncode.py /InputData${filename}

}

get_extension() {
filename=$1
IFS='.' read -ra mylist <<< "$filename"
extension="${mylist[1]}"
echo $extension
}

cd ..
#for c in `python3 DataStandardization/get_paths.py`; do
#    gunzip_if_gzipped InputData$c
#done
#for c in `python3 DataStandardization/get_paths.py`; do
#    echo gzipping $c
#    gzip InputData$c
#done
#for c in `python3 DataStandardization/get_paths.py`; do
#    imputing $c
#done
for c in `python3 DataStandardization/get_paths.py`; do
    one-hot_encoding $c
done
for c in `python3 DataStandardization/get_paths.py`; do
    IFS="/" read -ra mylist <<< "$c"
    data_type="${mylist[2]}"
    if [[ $data_type =~ ^(Covariate|Expression|RPPA|miRNA)$ ]]; then
        echo scaling ${c}
        scaling $c
    fi
done
