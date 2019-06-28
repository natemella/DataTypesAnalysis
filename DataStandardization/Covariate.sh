#!/usr/bin/env bash
set -e
. ./functions.sh
fileName="mmc1.xlsx"
web_url="https://www.cell.com/cms/10.1016/j.cell.2018.02.052/attachment/f4eb6b31-8957-4817-a41f-e46fd2a1d9c3/"
python_script=Covariate.py
folder="Covariate"
tcga_extension=".tsv"

download_and_organize_data $fileName $python_script $web_url $tcga_extension $folder


cd ../
cd DataStandardization/
python3 Class.py
