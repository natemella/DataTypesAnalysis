import os
from DataStandardization.util import *
import shutil

cwd = os.getcwd()
analysis_dir = os.path.join(*[cwd,"Analysis_Results"])

for data_type in os.listdir(analysis_dir):
    data_path = os.path.join(*[analysis_dir, data_type])
    for cancer in os.listdir(data_path):
        cancer_path = os.path.join(*[data_path, cancer])
        for endpoint in os.listdir(cancer_path):
            endpoint_path = os.path.join(*[cancer_path, endpoint])
            for iteration in os.listdir(endpoint_path):
                iteration_path = os.path.join(*[endpoint_path, iteration])
                for algorithm in os.listdir(iteration_path):
                    algorithm_path = os.path.join(*[iteration_path,algorithm])
                    for file in os.listdir(algorithm_path):
                        old_path = os.path.join(*[algorithm_path,file])
                        new_location_dr = os.path.join(*[analysis_dir, algorithm[:-2], data_type, cancer, endpoint, iteration])
                        new_location = os.path.join(*[new_location_dr,file])
                        print(old_path)
                        print(new_location)
                        if not os.path.exists(new_location_dr):
                            os.makedirs(new_location_dr)
                        os.rename(old_path, new_location)

    shutil.rmtree(data_path)
