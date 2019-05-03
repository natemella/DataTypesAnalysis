
import glob, gzip, os, shutil, sys
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve

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
datatype_directory = sys.argv[13]
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


out = "Description\tIteration\tAlgorithm\tAUROC\n"
for c in allDataToProcess:
    datasetID = c.split('\t')[0]
    classVar = c.split('\t')[1]
    data_files = c.split('\t')[2].split(',')

    input_data = list()
    dataset_path = datasetID + '/'
    class_path = dataset_path + 'Class/' + classVar + '.txt'

    for x in data_files:
        if datatype_directory == "Covariate":
            input_data.append(dataset_path + datatype_directory + '/' + x + ".txt")
        elif datatype_directory == "Expression":
            input_data.append(dataset_path + datasetID + ".txt.gz")

    input_data.append(class_path)


    for i in range(startIteration, 1 + stopIteration):
        print("Evaluating " + analysis + ' ' + datasetID + ' ' + classVar + ' ' + 'iteration' + str(i))
        path = '/Analysis_Results/' + analysis + '/' + datasetID + '/' + classVar + '/iteration' + str(i) + '/*/' + outFileToCheck

        executed_algos = glob.glob(path)
        executed_algos = [x.split('/')[4].replace('__', '/', 3) for x in executed_algos]
        executed_algos = set(executed_algos)



        for algo in executed_algos:
            algoName = algo.replace('/', '__')

            # Build the part of the command that tells ShinyLearner which data files to parse
            data_all = ''
            for d in input_data:
                data_all = data_all + '--data "' + d + '" \\\n\t\t'

            # Where will the output files be stored?
            metrics_file = currentWorkingDir + '/Analysis_Results/' + analysis + '/' + datasetID + '/' + classVar + '/iteration' + str(
                i) + '/' + algoName + '/Metrics.tsv'
            with open(metrics_file) as metrics_data:
                title_line = metrics_data.readline()
                AUROC_line = metrics_data.readline()
                metrics = AUROC_line.split('\t')
                AUROC = AUROC_line[-1]


            out += '{}__{}__{}\t{}\t{}'.format( analysis, datasetID, classVar, i, algoName)
            out += '\t' + str(AUROC) + '\n'

if len(aurocCommandFilePaths) == 0:
    print('All commands have been executed!')

resultsFilePath = 'Analysis_Results/{}'.format(analysis) + '.tsv'

if not os.path.exists(os.path.dirname(resultsFilePath)):
    os.makedirs(os.path.dirname(resultsFilePath))

    # Create the bash script
with open(resultsFilePath, 'w') as outFile:
    outFile.write(out + '\n')