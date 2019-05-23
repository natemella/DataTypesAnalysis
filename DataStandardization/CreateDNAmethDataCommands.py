with open("CancerTypes.txt") as input:
    output = open("DNA_MethylationFiles.sh", "w")
    for line in input:
        line = line.strip("\n")
        output.write(f"Rscript Prepare_Methylation_Data.R "
                     f"https://tcga.xenahubs.net/download/TCGA."
                     f"{line}.sampleMap/HumanMethylation450.gz {line}\n")


