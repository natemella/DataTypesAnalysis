#!/usr/bin/env bash
. ./functions.sh
fileName="1c8cfe5f-e52d-41ba-94da-f15ea1337efc"
python_script=SM.py
web_url="https://api.gdc.cancer.gov/data/"
tcga_extension=".tsv"
folder=SM
file_extension=".gz"
rename="True"

download_and_organize_data $fileName $python_script $web_url $tcga_extension $folder $file_extension $rename $1

