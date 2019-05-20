import os
import pandas as pd
currentWorkingDir = os.path.dirname(os.path.realpath(__file__))

RelevantTypes = ()


list = currentWorkingDir.split('/')
parent_directory = '/'.join(list[:-1])

def oneval(row,col):
    return row[col]
# All of the conditions upon which we will keep a row.

def filter_on_stuff(row, list, x, y):

    Event = oneval(row, list[0])
    Time = oneval(row, list[1])
    if (Time <= x and Event == 1) or Time >= y:
        return True
    return False

def give_labels(row, list, y):
    Time = oneval(row, list[1])
    if Time >= y:
        return 'True'
    return 'False'

endpoints = ("DFI","DSS","OS","PFI")

for x in next(os.walk(parent_directory + "/InputData"))[1]:
    for subdir in next(os.walk(parent_directory + "/InputData/" + x)):
        if "Covariate" in subdir:
            directory = f"{parent_directory}/InputData/{x}/Covariate"
            for filename in os.listdir(directory):
                if filename.endswith(".tsv"):
                    # f = open(f"{directory}/{filename}")
                    df = pd.read_csv(filepath_or_buffer=f"{directory}/{filename}", sep="\t", index_col="bcr_patient_barcode")

                    variables = df.columns.values
                    class_df = df[[value for value in variables if value.startswith(endpoints)]]
                    Class_dir = f"{parent_directory}/InputData/{x}/Class/"
                    if not os.path.exists(os.path.dirname(Class_dir)):
                        os.makedirs(os.path.dirname(Class_dir))

                    output = open(f'{Class_dir}/classlog.out','w')
                    #separate endpoints. Build df of just endpoint + endpoint.time
                    for val in endpoints:
                        one_class = class_df[[one_endpoint for one_endpoint in variables if one_endpoint.startswith(val)]]
                        output.write(f'Beginning parsing on {val}\n')
                        average = one_class[one_class.columns.values[1]].mean()
                        lower_cutoff = average - (180)  # 6 months
                        upper_cutoff = average + (180) # 6 months
                        output.write(f'DataFrame initial size is {one_class.size}\n'
                                     f'the average time value is {average}\n'
                                     f'the lower cutoff is {lower_cutoff}\n'
                                     f'the upper_cutoff is {upper_cutoff}\n')
                        one_class = one_class.loc[one_class.apply(filter_on_stuff, args=(one_class.columns.values, lower_cutoff,upper_cutoff), axis="columns")]
                        output.write(f'The final DataFrame size is {one_class.size}\n\n')
                        # give labels
                        df2 = one_class.apply(give_labels, args=(one_class.columns.values,upper_cutoff), axis="columns").map({'True': f'LT_{val}', 'False': f'ST_{val}'})
                        df2.to_csv(path_or_buf=f"{Class_dir}{val}.txt", sep="\t", header=True, na_rep="NA")



                    for var in variables:
                        if var.startswith(endpoints):
                            continue
                        else:
                            df[var].to_csv(path_or_buf=f"{directory}/{var}.txt", sep="\t", header=True, na_rep='NA')
                else:
                    continue
