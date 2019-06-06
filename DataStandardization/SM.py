import pandas as pd
import numpy as np
from util import *

def grab_cell_without_paren(row, col):
    return row[col].split("(")[0]

def grab_one_cell(row, col):
    return row[col]
# All of the conditions upon which we will keep a row.

def remove_sparse_rows(row):
    sift = grab_cell_without_paren(row, "SIFT")
    poly = grab_cell_without_paren(row, "PolyPhen")
    tumor = grab_one_cell(row, "Tumor_Sample_Barcode")
    if tumor.split('-')[1] not in relevant_codes:
        return False
    if sift == "deleterious":
        return True
    if sift == "deleterious_low_confidence" and (poly != "benign" or poly == "."):
        return True
    if poly == "possibly_damaging" and sift == ("." or not "tolerated" or "tolerated_low_confidence"):
        return True
    if poly == "." and sift == ".":
        return True
    return False

def chunk_filtering(df_chunk, step_num):
    df_chunk = df_chunk.loc[(df_chunk["FILTER"] == "PASS") & (df_chunk["NCALLERS"] >= 3) & (df_chunk["IMPACT"].isin(["MODERATE", "HIGH"]))]
    print(f"Completed Step 2.{step_num}")

    # apply conditions
    df_chunk = df_chunk.loc[df_chunk.apply(remove_sparse_rows, axis="columns")]
    return df_chunk

def build_df(df_chunk):
    chunk_list = []  # append each chunk df here
    step = 1
    # Each chunk is in df format
    for chunk in df_chunk:
        chunk_filter = chunk_filtering(chunk, step)
        step += 1
        chunk_list.append(chunk_filter)

    df_concat = pd.concat(chunk_list)
    return df_concat

def fill_dict(row, my_dict):
    key = grab_one_cell(row, "Tumor_Sample_Barcode")
    key = key[0:12]
    value = grab_one_cell(row, "Hugo_Symbol")
    if key.split('-')[1] not in reverse_tss_dict[cancer]:
        return
    if key not in my_dict:
        my_dict[key] = [value]
    else:
        my_dict[key].append(value)
    return

relevant_types = make_relevant_types_list()
abbreviations_dict = make_abbrevation_dict(relevant_types)

reverse_tss_dict = {}
for x in relevant_types:
    reverse_tss_dict[x] = []

relevant_codes = set()
with open("tss_codes.tsv") as codes:
    first_line = codes.readline()
    for x in codes:
        line = x.strip('\n').split('\t')
        if line[2] in relevant_types:
            relevant_codes.add(line[0])
            reverse_tss_dict[line[2]].append(line[0])

one_chunk = pd.read_csv("1c8cfe5f-e52d-41ba-94da-f15ea1337efc", sep='\t', low_memory=False, chunksize=500000)
print("Completed Step 1")
df = build_df(one_chunk)
# Make a dictionary where a Tumor_Sample_Barcode is the key to a list of genes. These are the genes where this tumor has a mutation

for cancer in reverse_tss_dict:

    dict = {}
    df.apply(fill_dict, args=(dict,), axis="columns")

    # the genes will become indexes and the Tumor_Sample_Barcodes will become columns
    final_df = pd.DataFrame(index=df.Hugo_Symbol.unique(), columns=dict.keys())

    # if a gene is in our list (from our dictionary) then we will assign it 1. Otherwise we will assign it a NaN for now.
    for x in dict:
        genes_with_mutations = pd.Series(dict[x], name=x)
        mutated_indexes = final_df.index.isin(genes_with_mutations)
        final_df[x] = np.where(mutated_indexes, 1, np.nan)

    final_df.reset_index()

    # count how many mutations per gene
    info = final_df.count(axis=1)

    # filter out the genes where they are mutated in fewer than two samples
    final_df = final_df.loc[info >= 2]

    # change NaN to 0 for gene in final_df.index.values and transpose df:
    final_df = final_df.fillna(value=0)
    final_df = final_df.T

    final_df = final_df.rename_axis("SampleID")
    final_df.to_csv(path_or_buf=('TCGA_' + abbreviations_dict[cancer] + '.tsv'), sep='\t')
