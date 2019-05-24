import os
import pandas as pd
from io import StringIO
import csv

currentWorkingDir = os.path.dirname(os.path.realpath(__file__))

RelevantTypes = ()

summary_df = pd.read_csv(filepath_or_buffer="summary.txt", sep='\t', index_col="CancerType")

list = currentWorkingDir.split('/')
parent_directory = '/'.join(list[:-1])

def oneval(row,col):
    return row[col]
# All of the conditions upon which we will keep a row.

def filter_on_stuff(row, list, x, y):

    Event = oneval(row, list[0])
    Time = oneval(row, list[1])
    # Index = row.name
    if (Time <= x and Event == 1) or Time >= y:
        return True
    return False

def give_labels(row, list, y, l, s):
    Time = oneval(row, list[1])
    if Time >= y:
        l.append(row.name)
        return 'True'
    s.append(row.name)
    return 'False'

endpoints = ("DFI","DSS","OS","PFI")

csvfile = StringIO()
header = ["CancerType"]
for x in endpoints:
    if x == "PFI":
        header.append(f'Num_of_Patients_Kept{x}')

header.append("SPFI")
header.append("LPFI")
writer = csv.writer(csvfile)
writer.writerow(header)
data = []
def make_value_column(df1,file_name,time_period):
    Value = df1[df1.columns.values[1]]
    Value = Value[~Value.isnull()].tolist()
    CancerType = [file_name.split('.')[0] for x in Value]
    Time = [time_period for x in Value]
    data = [CancerType,Value,Time]
    graph = pd.DataFrame.from_records(data).T
    return graph

DataFrames = []
for x in next(os.walk(parent_directory + "/InputData"))[1]:
    for subdir in next(os.walk(parent_directory + "/InputData/" + x)):
        if "Covariate" in subdir:
            directory = f"{parent_directory}/InputData/{x}/Covariate"
            for filename in os.listdir(directory):
                if filename.endswith(".tsv"):
                    df = pd.read_csv(filepath_or_buffer=f"{directory}/{filename}", sep="\t", index_col="bcr_patient_barcode")

                    variables = df.columns.values
                    class_df = df[[value for value in variables if value.startswith(endpoints)]]
                    Class_dir = f"{parent_directory}/InputData/{x}/Class/"
                    if not os.path.exists(os.path.dirname(Class_dir)):
                        os.makedirs(os.path.dirname(Class_dir))
                    row = [x]
                    #separate endpoints. Build df of just endpoint + endpoint.time
                    for val in endpoints:
                        one_class = class_df[[one_endpoint for one_endpoint in variables if one_endpoint.startswith(val)]]
                        if val == "PFI": # and filename== "TCGA_BRCA.tsv":
                           DataFrames.append(make_value_column(one_class,filename, "Before"))

                        average = one_class[one_class.columns.values[1]].mean()
                        lower_cutoff = average - (180)  # 6 months
                        upper_cutoff = average + (180) # 6 months
                        a = one_class.size

                        one_class = one_class.loc[one_class.apply(filter_on_stuff, args=(one_class.columns.values, lower_cutoff,upper_cutoff), axis="columns")]
                        if val == "PFI": # and filename == "TCGA_BRCA.tsv":
                           DataFrames.append(make_value_column(one_class, filename, "After"))

                        b = one_class.size

                        # give labels
                        LT = []
                        ST = []
                        df2 = one_class.apply(give_labels, args=(one_class.columns.values,upper_cutoff,LT,ST), axis="columns").replace(f'True',f'LT_{val}').replace('False',f'ST_{val}')
                        if val == "PFI":
                            row.append(str(len(LT) + len(ST)))
                            row.append(str(len(ST)))
                            row.append(str(len(LT)))

                        df2.to_csv(path_or_buf=f"{Class_dir}{val}.txt", sep="\t", header=True, na_rep="NA")
                    writer.writerow(row)

                    for var in variables:
                        if var.startswith(endpoints):
                            continue
                        else:
                            df[var].to_csv(path_or_buf=f"{directory}/{var}.txt", sep="\t", header=True, na_rep='NA')
                else:
                    continue

Final_Graph = pd.concat(DataFrames)
Final_Graph.columns = ["CancerType", "Value", "Time"]

Final_Graph.to_csv("results_for_graphing.csv", index=False)

csvfile.seek(0)

summary_df2 = pd.read_csv(csvfile, index_col="CancerType")
summary_df2 = summary_df2.apply(pd.to_numeric, errors="ignore")


frames = [summary_df2, summary_df]

result = pd.concat(frames, axis=1, sort='False')
result.to_csv(path_or_buf=f'result.tsv', sep='\t')


