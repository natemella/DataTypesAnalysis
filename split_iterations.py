import os
from DataStandardization.util import *
import shutil
import pandas as pd

cwd = os.getcwd()
analysis_dir = os.path.join(*[cwd,"Analysis_Results"])

for algo in os.listdir(analysis_dir):
    algo_path = os.path.join(*[analysis_dir, algo])
    for data_type in os.listdir(algo_path):
        data_path = os.path.join(*[algo_path, data_type])
        for cancer in os.listdir(data_path):
            cancer_path = os.path.join(*[data_path, cancer])
            for endpoint in os.listdir(cancer_path):
                endpoint_path = os.path.join(*[cancer_path, endpoint])
                for iteration in os.listdir(endpoint_path):
                    iteration_path = os.path.join(*[endpoint_path,iteration])
                    for file in os.listdir(iteration_path):
                        if file == "Log.txt":
                            continue
                        file_path = os.path.join(*[iteration_path,file])
                        i = 1
                        df = pd.read_csv(file_path, sep='\t')
                        while i <= 5:
                            if not os.path.exists(f"{iteration_path[:-1]}{i}"):
                                os.mkdir(f"{iteration_path[:-1]}{i}")
                            outdf = df.loc[(df.Iteration == i)]
                            outdf.Description = outdf.Description.replace("iteration1",f"iteration{i}")
                            output_path = os.path.join(*[f"{iteration_path[:-1]}{i}",file])
                            print(output_path)
                            outdf.to_csv(path_or_buf=output_path, sep="\t", index=False)
                            i +=1

