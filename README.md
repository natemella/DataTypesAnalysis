# DataTypesAnalysis
This repository contains code for analyzing multiple datatypes with multiple machine learning algorithms.
It uses another repository called ShinyLearner as well as docker in order to execute.

This README.md will discuss this repository's main script, createDockerCommands.py, and how that main script will interact with other scripts.

- createDockerCommands.py does 5 main things:
  - 1) It parses the algorithms file to find all the possilbe algorithms for the analysis
  - 2) It finds all the possible data combinations to process
  - 3) It checks to see if any of the anaylsis have already been done. If so it will not repeat the analysis
  - 4) Execute the anaylsis for each combination of dataset, algorith and iteration (through building bash scripts)
  - 5) Create a file that indicates the location of all the bash scripts that need to be executed
    
  In order to run createDockerCommands.py, you will need to build an Algorithms.txt and a Data_To_Process.txt. These two files should contain all of the algorithms and datatypes that you would like to use in your analysis.
  
- While running createDockerCommands.py, be sure to include the following parameters:
  - jobName 
  - startIteration
  - stopIteration
  - memoryGigs
  - hoursMax
  - numCores
  - algorithmsFilePath
  - outFileToCheck
  - dockeroutFilePath
  - shinyLearnerVersionNumber
  - datatype_directory_name
  
In order to run createDockerCommands.py, we recommend buidling a bash script that looks like the following:

 #!/bin/bash

 currentDir=$(pwd)

 dockerCommandsFile=Docker_Commands.sh
 startIteration=1
 stopIteration=2
 delay=1
 numJobs=2
 memoryGigs=100
 swapMemoryGigs=100
 hoursMax=1
 numCores=1
 outFileToCheck=Predictions.tsv
 version=496
 datatype=Covariate
 python3 createDockerCommands.1.py OutputData $startIteration $stopIteration $memoryGigs $swapMemoryGigs $hoursMax $numCores Algorithms.txt Data_To_Process.txt $outFileToCheck $dockerCommandsFile $version       $datatype

 jobLogFile=Analysis.job.log
 rm -f $jobLogFile
 parallel --retries 0 --shuf --progress --eta --delay $delay --joblog $jobLogFile -j $numJobs -- < $dockerCommandsFile
 
