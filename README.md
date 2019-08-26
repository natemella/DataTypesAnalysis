# DataTypesAnalysis

### Introduction
This repository contains code for an extensive work flow that uses multiple molecular datatypes with multiple machine 
learning algorithms for predicting cancer patient outcomes (PFI, OS, DSS, DFI).

This work flow uses an iterative approach to combine data types. In order to do this it first calculates the AUROC for 
each data type, cancer type, algorithm, fold,
 and iterations. It then determines which data types (or data type combinations) work best with each algorithm. It then reruns
 the analysis but with the "winning" data type (or data type combination) combined with the rest of the molecular data types. 

It uses another repository called [ShinyLearner](https://github.com/srp33/ShinyLearner) as well in order to execute. This workflow can be ran in a docker image or in
a slurm environment after installing ShinyLearner.

### Replicating Project
Any user can replicate our entire project including the downloading and filtration of our data by copying and pasting
 the following commands into the terminal of a super-computer linux system.
```bash
 git clone git@github.com:natemella/DataTypesAnalysis.git
 cd DataTypesAnalysis/
 bash RUN.sh
```
To only download our molecular and clinical data, copy and paste the following:
```bash
 git clone git@github.com:natemella/DataTypesAnalysis.git
 cd DataTypesAnalysis/DataStandardization/
 bash download_and_parse_all_data.sh
```

The full Pan-Cancer data set is also available at the (Open Science Framework) https://osf.io/3snep/.


  ![](Extra/Images/Input_Flow_Chart.png)
  
### Adjusting Cancer Types and Algorithms

To run our same analysis with differing cancer types and/or algorithms, edit the following files:

 - [Algorithms.txt](Algorithms.txt)
 - [CancerTypes.txt](DataStandardization/CancerTypes.txt)
 
### Adjusting Endpoints from Default (PFI)

To run our same analysis with OS, DSS or DFI predictions, simply execute the following command

```bash
 bash build_docker
 bash run_docker (specified endpoint: OS, DSS, or DFI)
```
For example, to run OS predictions type into the commandline

```bash
 bash build_docker
 bash run_docker OS
```
