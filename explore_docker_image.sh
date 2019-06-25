#!/usr/bin/env bash

docker run --rm -it --entrypoint=/bin/bash \
       -v "/InputData":"/DataTypesAnalysis/InputData" \
       -v "/Analysis_Results":"/DataTypesAnalysis/Analysis_Results" dta