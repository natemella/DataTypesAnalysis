import pandas as pd
import numpy as np

with open("CancerTypes.txt") as file:
    with open("abreviations.tsv") as abr:
        abreviations = [x.strip('\n') for x in file]
        RelevantTypes = [x.split('\t')[1].strip('\n') for x in abr if x.split('\t')[0] in abreviations]

TSSDictionary = {}
for x in RelevantTypes:
    TSSDictionary[x] = []

def split(row, col):
    return row[col].split("(")[0]

def makedict(row,col):
    return row[col]
# All of the conditions upon which we will keep a row.

def filter_on_stuff(row):
    sift = split(row, "SIFT")
    poly = split(row, "PolyPhen")
    tumor = makedict(row, "Tumor_Sample_Barcode")
    if tumor.split('-')[1] not in RelevantCodes:
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

def chunk_preprocessing(df_chunk, i):
    df_chunk = df_chunk.loc[(df_chunk["FILTER"] == "PASS") & (df_chunk["NCALLERS"] >= 3) & (df_chunk["IMPACT"].isin(["MODERATE", "HIGH"]))]
    print(f"Completed Step 2.{i}")

    # apply conditions
    df_chunk = df_chunk.loc[df_chunk.apply(filter_on_stuff, axis="columns")]
    return df_chunk

def build_df(df_chunk):
    chunk_list = []  # append each chunk df here
    i = 0
    # Each chunk is in df format
    for chunk in df_chunk:
        # perform data filtering
        chunk_filter = chunk_preprocessing(chunk, i)
        i += 1
        # Once the data filtering is done, append the chunk to list
        chunk_list.append(chunk_filter)

    # concat the list into dataframe
    df_concat = pd.concat(chunk_list)
    return df_concat

RelevantCodes = set()

#include the index column in each list


with open("TSS_CODES.tsv") as codes:
    first_line = codes.readline()
    for x in codes:
        line = x.strip('\n').split('\t')
        if line[2] in RelevantTypes:
            RelevantCodes.add(line[0])
            TSSDictionary[line[2]].append(line[0])

# So that the outputfile will have the correct names
Abbreviations_Dict = {}
with open("abreviations.tsv") as abr:
    first_line = abr.readline()
    for x in abr:
        list = x.strip('\n').split('\t')
        if list[1] in RelevantTypes:
            Abbreviations_Dict[list[1]] = list[0]

# read in data frame
# df = pd.read_csv("1c8cfe5f-e52d-41ba-94da-f15ea1337efc", sep='\t', low_memory=False)
# print("Completed Step 1")
#
# # only keep rows where Filter equals pass and Impact equals moderate or high
# df = df.loc[(df["FILTER"] == "PASS") & (df["NCALLERS"] >= 3) & (df["IMPACT"].isin(["MODERATE", "HIGH"]))]
# print("Completed Step 2")
#
#  # apply conditions
# df = df.loc[df.apply(filter_on_stuff, axis="columns")]
#
# print("Completed Step 3")

one_chunk = pd.read_csv("1c8cfe5f-e52d-41ba-94da-f15ea1337efc", sep='\t', low_memory=False, chunksize=500000)
print("Completed Step 1")
df = build_df(one_chunk)
# Make a dictionary where a Tumor_Sample_Barcode is the key to a list of genes. These are the genes where this tumor has a mutation


for Ctype in TSSDictionary:

    dict = {}

    def full_dict(row):
        key = makedict(row, "Tumor_Sample_Barcode")
        key = key[0:12]
        value = makedict(row, "Hugo_Symbol")
        if key.split('-')[1] not in TSSDictionary[Ctype]:
            return
        if key not in dict:
            dict[key] = [value]
        else:
            dict[key].append(value)
        return

    df.apply(full_dict, axis="columns")

    my_columns=[]


    # the genes will become indexes and the Tumor_Sample_Barcodes will become columns
    final_df = pd.DataFrame(index=df.Hugo_Symbol.unique(), columns=dict.keys())

    # if a gene is in our list (from our dictionary) then we will assign it 1. Otherwise we will assign it a NaN for now.

    for x in dict:
        a = pd.Series(dict[x], name=x)
        b = final_df.index.isin(a)
        final_df[x] = np.where(b, 1, np.nan)

    final_df.reset_index()

    # count how many mutations per gene
    info = final_df.count(axis=1)

    # filter out the genes where they are mutated in fewer than two samples
    final_df = final_df.loc[info >= 2]

    # change NaN to 0for gene in final_df.index.values:

    final_df = final_df.fillna(value=0)
    print('\n' + Ctype + " = " + Abbreviations_Dict[Ctype])
    print(final_df.columns.values)
    final_df = final_df.T
    final_df = final_df.rename_axis("SampleID")
    final_df.to_csv(path_or_buf=('TCGA_' + Abbreviations_Dict[Ctype] + '.tsv'), sep='\t')
