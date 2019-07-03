import sys
import os
import pandas as pd
from get_analysis_name import get_name

def get_analysis_file(ouput_dir, my_analysis):
    for file in os.listdir(ouput_dir):
        if file.replace(".tsv", "") == my_analysis:
            file = os.path.join(*[results_dir, file])
            return file

data_type_to_command = {}
data_type_to_command["Expression"] = " -e True"
data_type_to_command["CNV"] = " -n True"
data_type_to_command["Clinical"] = " -c True"
data_type_to_command["DNA_Methylation"] = " -d True"
data_type_to_command["miRNA"] = " -m True"
data_type_to_command["SM"] = " -s True"
data_type_to_command["RPPA"] = " -p True"

cwd = os.getcwd()
results_dir = os.path.join(*[cwd,"Permanent_Results"])
previous_combo = ' '.join(sys.argv[1:])
analysis = get_name(sys.argv[1:])
#calculate winning combination
input_file = get_analysis_file(results_dir, analysis)
df = pd.read_csv(input_file, sep="\t")
df = df.groupby(['CancerType','Algorithm','Description'], sort=True).mean()
df["Rank"] = df.groupby(['CancerType','Algorithm'])["AUROC"].rank()
winning_df = df.reset_index()
winning_df = winning_df.groupby(['Description'], sort=True)['Rank'].mean()
winner = winning_df.idxmax().split('+')[0]
new_combo = previous_combo + data_type_to_command[winner]
print(new_combo)
