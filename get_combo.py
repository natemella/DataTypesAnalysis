import sys
import os
import pandas as pd
# from get_analysis_name import get_name

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
previous_combo = ' '.join(sys.argv[2:])
# analysis = get_name(sys.argv[2:])
algo = sys.argv[1]
count = len([item for item in sys.argv[2:] if item != "True" and item != sys.argv[2]])
algo_nick_name = algo.split("__")[-1]
#calculate winning combination
# input_file = get_analysis_file(results_dir, analysis)
input_file = os.path.join(*[results_dir, f'combination_of_{count}.tsv'])
df = pd.read_csv(input_file, sep="\t")
df.AUROC = pd.to_numeric(df.AUROC)
df = df.loc[df.Algorithm == algo_nick_name]
# Use double groupby in order to get the average for each iterations
df = df.groupby(['CancerType','Algorithm','Description', 'Iteration'], sort=True).mean()
df = df.groupby(['CancerType','Algorithm','Description'], sort=True).mean()
df["Rank"] = df.groupby(['CancerType','Algorithm'])["AUROC"].rank()
winning_df = df.reset_index()
winning_df = winning_df.groupby(['Description'], sort=True)['Rank'].mean()
winner = winning_df.idxmax().split('+')[0]
new_combo = previous_combo + data_type_to_command[winner]
print(algo,new_combo)
