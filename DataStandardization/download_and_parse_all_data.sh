#!/usr/bin/env bash
set -e
bash Covariate.sh
echo -------------------
echo Finished Covariate
echo -------------------
bash miRNA.sh
echo -------------------
echo Finshed miRNA
echo -------------------
bash RPPA.sh
echo -------------------
echo Finished RPPA
echo -------------------
bash CNV.sh
echo -------------------
echo Finished CNV
echo -------------------
bash SM.sh
echo -------------------
echo Finished SM
echo -------------------
bash Expression.sh
echo -------------------
echo Finished Expression
echo -------------------
bash DNA_Methylation.sh
echo -------------------
echo Finished DNA Methylation
echo -------------------
python3 cutter.py -q True -c True
python3 cutter.py -c True
echo -------------------
echo Finished cutting
echo -------------------
bash scale_ohe_impute.sh
echo -------------------
echo Finished scale_ohe_impute
echo -------------------
