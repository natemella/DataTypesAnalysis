import glob, gzip, os, shutil, sys
from DataStandardization.util import *

analysis = sys.argv[1]
startIteration = int(sys.argv[2])
stopIteration = int(sys.argv[3])
memoryGigs = sys.argv[4]
swapMemoryGigs = sys.argv[5]
hoursMax = sys.argv[6]
numCores = sys.argv[7]
algorithmsFilePath = sys.argv[8]
dataToProcessFilePath = sys.argv[9]
outFileToCheck = sys.argv[10]
dockerOutFilePath = sys.argv[11]
shinyLearnerVersion = sys.argv[12]
scale_mode = sys.argv[13]
outer_folds = sys.argv[14]
inner_folds = sys.argv[15]
currentWorkingDir = os.path.dirname(os.path.realpath(__file__))

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
    class_path = [dataset_path,'Class',f'{classVar}.txt']
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
                data_all = data_all + f'--data "{d}" {line_end(3)}'

            # so that windows computers don't crash
            if path_delimiter() == '\\':
                _ = '\\' + '\\'
            else:
                _ = path_delimiter()
            # Where will the output files be stored?


            outDir = os.path.join(*[currentWorkingDir,"Analysis_Results",analysis, datasetID, classVar, 'iteration', str(i), algoName]) + _

            
            bash_args = {
                "outDir": outDir,
                "outFileToCheck": outFileToCheck,
                "memoryGigs": memoryGigs,
                "swapMemoryGigs": swapMemoryGigs,
                "currentWorkingDir": currentWorkingDir,
                "outDir": outDir,
                "shinyLearnerVersion": shinyLearnerVersion,
                "hoursMax": hoursMax,
                "data_all": data_all.rstrip(),
                "datasetID": datasetID,
                "classVar": classVar,
                "i": i,
                "outer_folds": outer_folds,
                "inner_folds": inner_folds,
                "algo": algo,
                "numCores": numCores,
            }
            out = """
if [ ! -f {outDir}{outFileToCheck} ]
then
    docker run --memory {memoryGigs}G --memory-swap {swapMemoryGigs}G --rm -i \\
        -v "{currentWorkingDir}/InputData":"/InputData" \\
        -v "{outDir}":"/OutputData" \\
        srp33/shinylearner:version{shinyLearnerVersion} \\
        timeout -s 9 {hoursMax}h \\
            "/UserScripts/nestedclassification_crossvalidation" \\
            {data_all}
            --description {datasetID}___{classVar}___iteration{i} \\
            --outer-folds {outer_folds} \\
            --inner-folds {inner_folds} \\
            --iterations 1 \\
            --classif-algo "AlgorithmScripts/Classification/{algo}*" \\
            --verbose false \\
            --seed {i} \\
            --ohe true \\
            --scale robust \\
            --impute true \\
            --num-cores 
fi
            """.format(**bash_args)
            # Build the bash script for this combination of dataset, algorithm, and iteration
            if scale_mode != "True":
                out = out.replace(f'--scale robust {line_end(2)}','')

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
                        dockerOutFile.write(f"bash {command}\n")
