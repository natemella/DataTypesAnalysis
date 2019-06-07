#!/usr/bin/env bash

set -e
. ./functions.sh
fileName="TCGA-RPPA-pancan-clean.xena.gz"
python_script=RPPA.py
web_url="https://pancanatlas.xenahubs.net/download"
tcga_extension=".tsv"
folder=RPPA

download_and_organize_data $fileName $python_script $web_url $tcga_extension $folder

fileName="TCGA-RPPA-pancan-clean.xena"

