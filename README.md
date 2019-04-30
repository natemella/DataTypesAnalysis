# DataTypesAnalysis
This repository contains code for analyzing multiple datatypes with multiple machine learning algorithms.
It uses another repository called ShinyLearner as well as docker in order to execute.

This README.md will discuss this repository's main script, createDockerCommands.py.

- createDockerCommands.py does 5 main things:
  - 1) It parses the algorithms file to find all the possilbe algorithms for the analysis
  - 2) It finds all the possible data combinations to process
  - 3) It checks to see if any of the anaylsis have already been done. If so it will not repeat the analysis
  - 4) Execute the anaylsis for each combination of dataset, algorith and iteration (through building bash scripts)
  - 5) Create a file that indicates the location of all the bash scripts that need to be executed
    
  
  It's parameters include:
  - analysis 
  - startIteration
  - stopIteration
  - memoryGigs
  - hoursMax
  - numCores
  - algorithmsFilePath
  - outFileToCheck
  - dockeroutFilePath
  

