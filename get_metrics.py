import glob, gzip, os, shutil
import argparse

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
    default="513",
    help="Version of ShinyLearner docker image to use. See https://hub.docker.com/r/srp33/shinylearner/tags for "
         "published versions."
)


args = parser.parse_args()

analysis = args.analysis
startIteration = args.start_iteration
stopIteration = args.stop_iteration
algorithmsFilePath = args.algorithms_path
dataToProcessFilePath = args.data_path
outFileToCheck = args.check_file
dockerOutFilePath = args.outfile

shinyLearnerVersion = args.shiny_learner_version
currentWorkingDir = os.path.dirname(os.path.realpath(__file__))

aurocCommandFilePaths = []

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
if os.path.exists(analysis + '_Commands/'):
    shutil.rmtree(analysis + '_Commands/')


out = "Description\tCancerType\tClassType\tIteration\tfold\tAlgorithm\tDefaultParameters\tAUROC\n"
predections_results = os.path.join(*["Analysis_Results","Total_Predictions.tsv.gz"])

input_data = []
class_path = ''
for c in allDataToProcess:
    datasetID = c.split('\t')[0]
    classVar = c.split('\t')[1]

    input_data = list()
    dataset_path = datasetID + '/'
    class_path = dataset_path + 'Class/' + classVar + '.txt'
    # grab the data types
    datatype_directory = c.split('\t')[2].split(',')
    number_of_datatypes = len(datatype_directory)

    # grab the data files for each data type
    for i in range(0, number_of_datatypes):
        datatype = datatype_directory[i]
        input_files = c.split('\t')[3 + i].split(',')
        for x in input_files:
            if datatype == "Expression":
                input_data.append(dataset_path + datatype + '/' + x + '.txt.gz')
            else:
                input_data.append(dataset_path + datatype + '/' + x + '.txt')

    input_data.append(class_path)


    for i in range(startIteration, 1 + stopIteration):
        print("Evaluating " + analysis + ' ' + datasetID + ' ' + classVar + ' ' + 'iteration' + str(i))
        path = 'Analysis_Results/' + analysis + '/' + datasetID + '/' + classVar + '/iteration' + str(i) + '/*/' + outFileToCheck
        executed_algos = glob.glob(path)
        executed_algos = [x.split('/')[5].replace('__', '/', 3) for x in executed_algos]
        executed_algos = set(executed_algos)
        print(executed_algos)
        for algo in executed_algos:
            rootAlgo = algo.split('/')
            default_bool = 0
            if rootAlgo[-1].startswith("default"):
                default_bool = 1
            print(f'root algo = {rootAlgo}')
            rootAlgo = rootAlgo[-2]
            algoName = algo.replace('/', '__')

            # Build the part of the command that tells ShinyLearner which data files to parse
            data_all = ''
            for d in input_data:
                data_all = data_all + '--data "' + d + '" \\\n\t\t'

            # Where will the output files be stored?
            metrics_file = os.path.join(*[currentWorkingDir,'Analysis_Results',analysis,datasetID,classVar,f'iteration{str(i)}',algoName,'Metrics.tsv'])
            predictions_file = os.path.join(*[currentWorkingDir,'Analysis_Results',analysis,datasetID,classVar,f'iteration{str(i)}',algoName,'Predictions.tsv'])
            print(metrics_file)
            with open(metrics_file) as metrics_data:
                title_line = metrics_data.readline()
                for line in metrics_data:
                    metrics = line.strip('\n').split('\t')
                    if metrics[-2] == "AUROC":
                        AUROC = metrics[-1]
                        fold = metrics[2]
                        out += f'{analysis}\t{datasetID}\t{classVar}\t{i}\t{fold}\t{rootAlgo}\t{default_bool}'
                        out += '\t' + str(AUROC) + '\n'
            with open(predictions_file, 'r') as content_file:
                content = content_file.read()
                with gzip.open(predections_results, 'a') as output:
                    output.write(content)

if len(aurocCommandFilePaths) == 0:
    print('All commands have been executed!')

resultsFilePath = 'Analysis_Results/{}'.format(analysis) + '.tsv'

if not os.path.exists(os.path.dirname(resultsFilePath)):
    os.makedirs(os.path.dirname(resultsFilePath))

    # Create the bash script
with open(resultsFilePath, 'w') as outFile:
    outFile.write(out)