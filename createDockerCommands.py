import glob, gzip, os, shutil, sys

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

currentWorkingDir = os.path.dirname(os.path.realpath(__file__))

dockerCommandFilePaths = []

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

for c in allDataToProcess:
  datasetID = c.split('\t')[0]
  classVar = c.split('\t')[1]

  input_data = list()
  dataset_path = 'Input/' + datasetID + '/'
  expression_path = dataset_path + datasetID + '.txt.gz'
  class_path = dataset_path + 'Class/' + classVar + '.txt'

  input_data.append(expression_path)
  input_data.append(class_path)

  for i in range(startIteration, 1+stopIteration):
    print(analysis + ' ' + datasetID + ' ' + classVar + ' ' + 'iteration' + str(i))
    path = analysis + '/' + datasetID + '/' + classVar + '/iteration' + str(i) + '/*/' + outFileToCheck

    executed_algos = glob.glob(path)
    executed_algos = [x.split('/')[4].replace('__','/',3) for x in executed_algos]
    executed_algos = set(executed_algos)

    not_executed_algos = allAlgorithms - executed_algos

  for algo in not_executed_algos:
    algoName = algo.replace('/','__')

    # Build the part of the command that tells ShinyLearner which data files to parse
    data_all = ''
    for d in input_data:
      data_all = data_all + '--data "/InputData/' + d + '" '

    # Where will the output files be stored?
    outDir = '/Analysis/BiomarkerBenchmark/' + analysis + '/' + datasetID + '/' + classVar + '/iteration' + str(i) + '/' + algoName + '/'

    # Build the bash script for this combination of dataset, algorithm, and iteration
    out = 'if [ ! -f ' + outDir + outFileToCheck + ' ]\nthen\n  docker run --memory ' + memoryGigs + 'G --memory-swap ' + swapMemoryGigs + 'G --rm -i -v "/Analysis/BiomarkerBenchmark/":/InputData -v "' + outDir + '":/OutputData srp33/shinylearner:version484 timeout -s 9 ' + hoursMax + 'h "/UserScripts/classification_montecarlo" ' + data_all + '--description ' + datasetID + '___' + classVar + '___iteration' + str(i) + ' --iterations 1 --classif-algo "AlgorithmScripts/Classification/' + algo + '*" --output-dir "/OutputData" --seed ' + str(i) + ' --verbose false --num-cores ' + numCores + '\nfi'

    # This is where the bash script will be stored
    commandFilePath = analysis + '_Commands/{}/{}/iteration{}/{}.sh'.format(datasetID, classVar, i, algoName)

    # Create the directory, if necessary, where the bash script will be stored
    if not os.path.exists(os.path.dirname(commandFilePath)):
      os.makedirs(os.path.dirname(commandFilePath))

    # Create the bash script
    with open(commandFilePath, 'w') as outFile:
      outFile.write(out + '\n')

    dockerCommandFilePaths.append(commandFilePath)

if len(dockerCommandFilePaths) == 0:
    print('All commands have been executed!')
else:
    # Create a file that indicates the location of all the bash scripts that need to be executed
    with open(dockerOutFilePath, 'w') as dockerOutFile:
        for command in dockerCommandFilePaths:
            dockerOutFile.write("bash {}\n".format(command))
