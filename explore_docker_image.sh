#!/usr/bin/env bash

docker run --rm -it --entrypoint=/bin/bash \
       -v "$(pwd)/InputData/":"~/DataTypesAnalysis/InputData" \
       -v "$(pwd)/Analysis_Results":"~/DataTypesAnalysis/Analysis_Results" dta