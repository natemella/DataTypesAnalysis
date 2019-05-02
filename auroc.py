
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
# if os.path.exists(analysis + '_Commands/'):
#     shutil.rmtree(analysis + '_Commands/')

# if os.path.exists(analysis + '_AUROC/'):
#     shutil.rmtree(analysis + '_AUROC/')

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
        path = analysis + '/' + datasetID + '/' + classVar + '/iteration' + str(i) + '/*/' + outFileToCheck

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
            predictions_file = currentWorkingDir + "/" + analysis + '/' + datasetID + '/' + classVar + '/iteration' + str(
                i) + '/' + algoName + '/Predicitions.tsv'

            # Build the python script for this combination of dataset, algorithm, and iteration
            out = "# roc curve from sklearn.datasets import make_classification\n" \
                  "from sklearn.linear_model import LogisticRegression\n" \
                  "from sklearn.model_selection import train_test_split\n" \
                  "from sklearn.metrics import roc_curve\n" \
                  "from matplotlib import pyplot\n" \
                  "import pandas as pd\n" \
                  "df = pd.read_tsv(\"" + predictions_file + \
                  "\")\n" \
                  "print(df)\n" \
                  "# generate 2 class dataset\n" \
                  "#X, y = make_classification(n_samples=1000, n_classes=2, random_state=1)\n" \
                  "# split into train/test sets\n" \
                  "#trainX, testX, trainy, testy = train_test_split(X, y, test_size=0.5, random_state=2)\n" \
                  "# fit a model\n" \
                  "#model = LogisticRegression()\n" \
                  "#model.fit(trainX, trainy)\n" \
                  "# predict probabilities\n" \
                  "#probs = model.predict_proba(testX)\n" \
                  "# keep probabilities for the positive outcome only\n" \
                  "#probs = probs[:, 1]\n" \
                  "# calculate roc curve\n" \
                  "#fpr, tpr, thresholds = roc_curve(testy, probs)\n" \
                  "# plot no skill\n" \
                  "#pyplot.plot([0, 1], [0, 1], linestyle='--')\n" \
                  "# plot the roc curve for the model\n" \
                  "#pyplot.plot(fpr, tpr)\n" \
                  "# show the plot\n" \
                  "#pyplot.show()\n" \
 \
            # This is where the bash script will be stored
            commandFilePath = '{}/{}/{}/{}/iteration{}/{}AUROC.py'.format(currentWorkingDir, analysis, datasetID, classVar, i, algoName)

            # Create the directory, if necessary, where the bash script will be stored
            if not os.path.exists(os.path.dirname(commandFilePath)):
                os.makedirs(os.path.dirname(commandFilePath))

            # Create the bash script
            with open(commandFilePath, 'w') as outFile:
                outFile.write(out + '\n')

            aurocCommandFilePaths.append(commandFilePath)

            # Create a file that indicates the location of all the python scripts that need to be executed
            with open(dockerOutFilePath, 'w') as dockerOutFile:
                for command in aurocCommandFilePaths:
                    dockerOutFile.write("python3 {}\n".format(command))

if len(aurocCommandFilePaths) == 0:
    print('All commands have been executed!')

