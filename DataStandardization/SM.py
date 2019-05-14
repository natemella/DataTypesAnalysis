import pandas as pd

# read in data frame
df = pd.read_csv("sm.tsv", sep='\t')
# only keep rows where Filter equals pass and Impact equals moderate or high
df = df.loc[(df["FILTER"] == "PASS") & (df["NCALLERS"] >= 3) & (df["IMPACT"].isin(["MODERATE", "HIGH"]))]

# SIFT and PolyPhen columns have numbers in their values that we don't want to look at. (i.e. deleterious(1.03))
# so we'll split the value

def split(row, col):
    return row[col].split("(")[0]

# All of the conditions upon which we will keep a row.

def filter_on_stuff(row):
    sift = split(row, "SIFT")
    poly = split(row, "PolyPhen")
    if sift == "deleterious":
        return True
    if sift == "deleterious_low_confidence" and (poly != "benign" or poly == "."):
        return True
    if poly == "possibly_damaging" and sift == ("." or not "tolerated" or "tolerated_low_confidence"):
        return True
    if poly == "." and sift == ".":
        return True
    return False

 # apply conditions
df = df.loc[df.apply(filter_on_stuff, axis="columns")]

dict = {}

def makedict(row,col):
    return row[col]

# Make a dictionary where a Tumor_Sample_Barcode is the key to a list of genes. These are the genes where this tumor has a mutation
def full_dict(row):
    key = makedict(row, "Tumor_Sample_Barcode")
    value = makedict(row, "Hugo_Symbol")
    if key not in dict:
        dict[key] = [value]
    else:
        dict[key].append(value)
    return


df.apply(full_dict, axis="columns")

my_columns=[]

# check to see if there are at least two mutations in each Tumor Sample Barcode

for x in dict.keys():
    if len(dict[x]) > 2:
        my_columns.append(x)

# the genes will become indexes and the Tumor_Sample_Barcodes will become columns
final_df = pd.DataFrame(index=df.Hugo_Symbol, columns=my_columns)

# if a gene is in our list (from our dictionary) then we will assign it 1. Otherwise we will assign it a NaN for now.
for gene in final_df.index.values:
    for patient in final_df.columns.values:
        if gene in dict[patient]:
            final_df.at[gene, patient] = 1

final_df.reset_index()

# get rid of duplicate genes in data frame
final_df = final_df.groupby(["Hugo_Symbol"], sort=False).max()

# count how many mutations per gene
info = final_df.count(axis=1)

# filter out the genes where they are mutated in fewer than two samples
final_df = final_df.loc[info >= 2]

# change NaN to 0
final_df = final_df.fillna(value=0)

print(final_df)

