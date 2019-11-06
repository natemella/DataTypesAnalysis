#!/usr/bin/env bash

Rscript combo_diff.R
Rscipt data_type.R ../Permanent_Results/combination_of_0.tsv
wget "https://ars.els-cdn.com/content/image/1-s2.0-S0092867418302290-mmc1.xlsx"
Rscipt violin_cancer_type.R ../Permanent_Results/combination_of_0.tsv
Rscript model_type.R ../Permanent_Results/combination_of_0.tsv
