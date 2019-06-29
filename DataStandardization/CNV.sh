#!/usr/bin/env bash

. ./functions.sh

fileName="broad.mit.edu_PANCAN_Genome_Wide_SNP_6_whitelisted.gene.xena.gz"
python_script=miRNA.py
web_url="https://pancanatlas.xenahubs.net/download"
tcga_extension=".ttsv"
folder=CNV
force=$1
echo RUNNING BASH SCRIPT FOR CNV but using same python script as miRNA to process the data

download_and_organize_data $fileName $python_script $web_url $tcga_extension $folder "" "" $force

