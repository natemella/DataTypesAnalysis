import os
import pandas as pd
currentWorkingDir = os.path.dirname(os.path.realpath(__file__))

RelevantTypes = ()


list = currentWorkingDir.split('/')
parent_directory = '/'.join(list[:-1])
# print("parent directory = " + parent_directory)
# print("current directory = " + currentWorkingDir)

# for CancerType, DataType, File in os.walk(parent_directory + '/InputData'):
#     print(CancerType)

# print(next(os.walk(parent_directory + "/InputData"))[1])
for x in next(os.walk(parent_directory + "/InputData"))[1]:
    for subdir in next(os.walk(parent_directory + "/InputData/" + x)):
        if "Covariate" in subdir:
            directory = f"{parent_directory}/InputData/{x}/Covariate"
            for filename in os.listdir(directory):
                if filename.endswith(".tsv"):
                    # f = open(f"{directory}/{filename}")
                    df = pd.read_csv(filepath_or_buffer=f"{directory}/{filename}", sep="\t", index_col="bcr_patient_barcode")
                    variables = df.columns.values
                    for var in variables:
                        if var.startswith(("DFI","DSS","OS","PFI")):
                            Class_dir = f"{parent_directory}/InputData/{x}/Class/"
                            if not os.path.exists(os.path.dirname(Class_dir)):
                                os.makedirs(os.path.dirname(Class_dir))
                            df[var].to_csv(path_or_buf=f"{Class_dir}/{var}.txt", sep="\t", header=True)
                        else:
                            df[var].to_csv(path_or_buf=f"{directory}/{var}.txt", sep="\t", header=True)
                else:
                    continue
        #     print(parent_directory + "/InputData/" + x)
