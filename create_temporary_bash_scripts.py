import argparse
import glob, gzip, os, shutil, sys
from DataStandardization.util import *

parser = argparse.ArgumentParser(description="Create bash scripts for running ShinyLearner with docker.")
parser.add_argument(
    "analysis",
    help="Output name of the analysis."
)
parser.add_argument(
    "data_path",
    help=(
        "Path to a tab-separated file that gives paths for the data to be processed. " 
        "No header, Columns=[CancerType, Class, DataTypes (comma-separated), FilePaths (comma-separated, "
        "one column for each DataType)]. "
        "Generate these files with `DataStandardization/create_data_to_process_files.py`. "
    )
)
parser.add_argument(
    "-s",
    "--start-iteration",
    type=int,
    default=1,
    help="Iteration to start on."
)
parser.add_argument(
    "-e",
    "--stop-iteration",
    type=int,
    default=1,
    help="Iteration to end on."
)
parser.add_argument(
    "-m",
    "--memory-gigs",
    type=int,
    default=200,
    help="Amount of memory to allocate to docker in GB."
)
parser.add_argument(
    "-w",
    "--swap-memory-gigs",
    type=int,
    default=200,
    help="Amount of swap to allocate to docker in GB."
)
parser.add_argument(
    "-t",
    "--hours-max",
    type=int,
    default=5,
    help="Number of hours to run before timing out."
)
parser.add_argument(
    "-c",
    "--cores",
    type=int,
    default=1,
    help="Number of cores to allocate to docker."
)
parser.add_argument(
    "-a",
    "--algorithms-path",
    default="Algorithms.txt",
    help="Path to a newline-separated list of algorithms to run."
)
parser.add_argument(
    "-x",
    "--check-file",
    default="Predictions.tsv",
    help="Path to the output file. Used to check if analysis has previously been completed."
)
parser.add_argument(
    "-o",
    "--outfile",
    default="Docker_Commands.sh",
    help="Path to save the bash script to run all the docker scripts."
)
parser.add_argument(
    "-l",
    "--shiny-learner-version",
    default="515",
    help="Version of ShinyLearner docker image to use. See https://hub.docker.com/r/srp33/shinylearner/tags for "
         "published versions."
)
parser.add_argument(
    "--scale-mode",
    default="False",
    help="Whether to scale the input data to [-1.0, 1.0] before learning."
)
parser.add_argument(
    "-u",
    "--outer-folds",
    type=int,
    default=10,
    help="Number of outer folds to use in nested cross-validation for parameter optimization."
)
parser.add_argument(
    "-i",
    "--inner-folds",
    type=int,
    default=5,
    help="Number of inner folds to use in nested cross-validation for parameter optimization."
)

args = parser.parse_args()

analysis = args.analysis
startIteration = args.start_iteration
stopIteration = args.stop_iteration
algorithmsFilePath = args.algorithms_path
dataToProcessFilePath = args.data_path
outFileToCheck = args.check_file
dockerOutFilePath = args.outfile
current_working_dir = os.path.dirname(os.path.realpath(__file__))

dockerCommandFilePaths = []

def line_end(num_of_tabs=0):
    my_string = "\\\n"
    for x in range(num_of_tabs):
        my_string += ' '*4
    return my_string

# Parse the algorithms file to find all possible algorithms
with open(algorithmsFilePath, 'r') as f:
    allAlgorithms = f.read().splitlines()
allAlgorithms = [x.replace('AlgorithmScripts/Classification/', '') for x in allAlgorithms if not x.startswith("#")]
allAlgorithms = [x.split("__")[0] for x in allAlgorithms]
allAlgorithms = set(allAlgorithms)

# Find all possible data combinations to process
with open(dataToProcessFilePath, 'r') as g:
    allDataToProcess = [x for x in g.read().splitlines() if not x.startswith("#")]

# Remove directory that contains the bash scripts that need to be executed
#   for each combination of dataset, algorithm, and iteration.
if os.path.exists(f'{analysis}_Commands{path_delimiter()}'):
    shutil.rmtree(f'{analysis}_Commands{path_delimiter()}')

for c in allDataToProcess:
    datasetID = c.split('\t')[0]
    classVar = c.split('\t')[1]

    input_data = list()
    dataset_path =  f'{datasetID}{path_delimiter()}'
    class_path = [dataset_path,'Class',f'{classVar}.tsv']
    class_path = os.path.join(*class_path)

    # grab the data types
    datatype_directory = c.split('\t')[2].split(',')
    number_of_datatypes = len(datatype_directory)
    # grab the data files for each data type

    for i in range(0, number_of_datatypes):
        datatype = datatype_directory[i]
        input_files = c.split('\t')[3 + i].split(',')
        for x in input_files:
                input_data.append(f'{dataset_path}{datatype}{path_delimiter()}{x}')



    input_data.append(class_path)

    not_executed_algos = set()

    for i in range(startIteration, 1+stopIteration):
        print(f'{analysis} {datasetID} {classVar} iteration {str(i)}')
        path = ['Analysis_Results',analysis, datasetID, classVar, 'iteration', str(i), '*' ,outFileToCheck]
        path = os.path.join(*path)
        executed_algos = glob.glob(path)
        executed_algos = [path_to_list(x)[5].replace('__', path_delimiter(), 3) for x in executed_algos]
        executed_algos = set(executed_algos)

        not_executed_algos = allAlgorithms - executed_algos


        for algo in not_executed_algos:
            algoName = algo.replace('/','__')

            # Build the part of the command that tells ShinyLearner which data files to parse
            data_all = ''
            for d in input_data:
                data_all = data_all + f'--data "{d}" {line_end(1)}'

            # so that windows computers don't crash
            if path_delimiter() == '\\':
                _ = '\\' + '\\'
            else:
                _ = path_delimiter()
            # Where will the output files be stored?


            out_dir = os.path.join(*[current_working_dir, "Analysis_Results", analysis, datasetID, classVar, f'iteration{i}', algoName]) + _

            
            bash_args = {
                "outFileToCheck": args.check_file,
                "memoryGigs": args.memory_gigs,
                "swapMemoryGigs": args.swap_memory_gigs,
                "currentWorkingDir": current_working_dir,
                "outDir": out_dir,
                "shinyLearnerVersion": args.shiny_learner_version,
                "hoursMax": args.hours_max,
                "data_all": data_all.rstrip(),
                "analysis": analysis,
                "datasetID": datasetID,
                "classVar": classVar,
                "i": i,
                "outer_folds": args.outer_folds,
                "inner_folds": args.inner_folds,
                "algo": algo,
                "numCores": args.cores,
            }
            out = """
#!/bin/bash

#SBATCH --time=04:00:00   # walltime
#SBATCH --ntasks=1   # number of processor cores (i.e. tasks)
#SBATCH --nodes=1   # number of nodes
#SBATCH -C 'rhel7'   # features syntax (use quotes): -C 'a&b&c&d'
#SBATCH --mem-per-cpu=16384M   # memory per CPU core


cd ../
if [ ! -f {outDir}{outFileToCheck} ]
then
    if [ "$(ls -A OutputData/)" ]; then
        rm OutputData/*
    else
        echo PROCESSING {analysis}__{datasetID}___{classVar}___iteration{i}
    fi
    "UserScripts/nestedclassification_crossvalidation" \\
    {data_all}
    --description {analysis}__{datasetID}___{classVar}___iteration{i} \\
    --outer-folds {outer_folds} \\
    --inner-folds {inner_folds} \\
    --iterations 1 \\
    --classif-algo "AlgorithmScripts/Classification/{algo}*" \\
    --verbose false \\
    --seed {i} \\
    --ohe false \\
    --scale none \\
    --impute false \\
    --num-cores {numCores}
fi
for file in `ls OutputData`; do
    mkdir -p {outDir}; mv OutputData/$file $_
done
            """.format(**bash_args)
            # Build the bash script for this combination of dataset, algorithm, and iteration
            if args.scale_mode != "True":
                out = out.replace(f'--scale robust {line_end(2)}','')
            if algo == "tsv/keras/dnn/" or algo == "tsv/sklearn/logistic_regression/":
                out = out.replace("#!/bin/bash\n\n","")
                out = "#!/bin/bash\n\n#SBATCH --gres=gpu:1" + out
            else:
                out = out.replace("\n#!","#!")
            # This is where the bash script will be stored
            commandFilePath = [f'{analysis}_Commands',datasetID,classVar,f'iteration{i}',f'{algoName}.sh']
            commandFilePath = os.path.join(*commandFilePath)
            # Create the directory, if necessary, where the bash script will be stored
            if not os.path.exists(os.path.dirname(commandFilePath)):
                os.makedirs(os.path.dirname(commandFilePath))

            # Create the bash script
            with open(commandFilePath, 'w') as outFile:
                outFile.write(f'{out}\n')

            dockerCommandFilePaths.append(commandFilePath)

if len(dockerCommandFilePaths) == 0:
        print('All commands have been executed!')
else:
        # Create a file that indicates the location of all the bash scripts that need to be executed
        with open(dockerOutFilePath, 'a') as dockerOutFile:
                for command in dockerCommandFilePaths:
                        dockerOutFile.write(f"sbatch {command}\n")
                dockerOutFile.write("wait")
