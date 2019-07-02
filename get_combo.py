import sys
import os
import pandas as pd

def get_analysis_file(ouput_dir, my_analysis):
    for file in os.listdir(ouput_dir):
        if file.replace(".tsv", "") == my_analysis:
            file = os.path.join(*[results_dir, file])
            return file


cwd = os.getcwd()
results_dir = os.path.join(*[cwd,"Permanent_Results"])


previous_combo = ' '.join(sys.argv[1:-1])
analysis = sys.argv[-1]

data_type_to_command = {}
data_type_to_command["Expression"] = " -e True"
data_type_to_command["CNV"] = " -n True"
data_type_to_command["Clinical"] = " -c True"
data_type_to_command["DNA_Methylation"] = " -d True"
data_type_to_command["miRNA"] = " -m True"
data_type_to_command["SM"] = " -s True"
data_type_to_command["RPPA"] = " -p True"

#calculate winning combination
input_file = get_analysis_file(results_dir, analysis)
df = pd.read_csv(input_file, sep="\t")
print(df.groupby(['CancerType','Algorithm','Description'], sort=True).mean())

winner = "Expression"
new_combo = previous_combo + data_type_to_command[winner]
print(new_combo)
print(analysis)
