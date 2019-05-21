import os
import pandas as pd

currentWorkingDir = os.path.dirname(os.path.realpath(__file__))

RelevantTypes = ()


list = currentWorkingDir.split('/')
parent_directory = '/'.join(list[:-1])


endpoints = ("DFI","DSS","OS","PFI")


for x in next(os.walk(parent_directory + "/InputData"))[1]:
    for subdir in next(os.walk(parent_directory + "/InputData/" + x)):
        if "Covariate" in subdir:
            directory = f"{parent_directory}/InputData/{x}/Covariate"
            for filename in os.listdir(directory):
                if filename.endswith(".tsv"):
                    Class_dir = f"{parent_directory}/InputData/{x}/Class/"
                    if not os.path.exists(os.path.dirname(Class_dir)):
                        os.makedirs(os.path.dirname(Class_dir))
                    #separate endpoints. Build df of just endpoint + endpoint.time

                else:
                    continue



