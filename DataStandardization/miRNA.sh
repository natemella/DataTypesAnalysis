#!/usr/bin/env bash
set -e
. ./functions.sh
fileName="pancanMiRs_EBadjOnProtocolPlatformWithoutRepsWithUnCorrectMiRs_08_04_16.xena.gz"
python_script=miRNA.py
web_url="https://pancanatlas.xenahubs.net/download"
tcga_extension=".ttsv"
folder=miRNA

download_and_organize_data $fileName $python_script $web_url $tcga_extension $folder

