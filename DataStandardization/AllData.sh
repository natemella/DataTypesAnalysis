#!/usr/bin/env bash
-e
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
echo --------------------
bash SM.sh
echo -------------------
echo Finished SM
echo -------------------
bash Expression.sh
echo -------------------
echo Finished Expression
echo -------------------
