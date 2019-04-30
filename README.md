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
  
  For an example of an Algorithms.txt file, click here: ![](DataTypesAnalysis/blob/master/Algorithms.example.txt)
  
  For an example of a Data_To_Process.txt file, click here: ![](DataTypesAnalysis/edit/master/Data_To_Process.txt)
  
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
  
In order to run createDockerCommands.py, we recommend buidling a bash script. For an example please click here https://github.com/natemella/DataTypesAnalysis/blob/master/exe_analysis_example
 
See the flow chart below to understand how this repository expects the data to be stored.
![](Images/Input_Flow_Chart.png)
