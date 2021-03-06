#!/usr/bin/env bash

if [ ! -d "InputData/" ]; then
mkdir InputData/
fi

if [ ! -d "Analysis_Results/" ]; then
mkdir Analysis_Results/
fi

if [ ! -d "Permanent_Results/" ]; then
mkdir Permanent_Results/
fi

docker run --rm --memory 200G --memory-swap 200G -it --entrypoint=/bin/bash \
       -v "$(pwd)/InputData/":"/DataTypesAnalysis/InputData/" \
       -v "$(pwd)/Analysis_Results/":"/DataTypesAnalysis/Analysis_Results/" \
       -v "$(pwd)/Permanent_Results/":"/DataTypesAnalysis/Permanent_Results/" dta