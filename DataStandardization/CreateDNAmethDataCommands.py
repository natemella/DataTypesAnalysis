with open("CancerTypes.txt") as input:
    output = open("DNA_MethylationFiles.sh", "w")
    for cancerType in input:
        cancerType = cancerType.strip("\n")
        output.write(f"mkdir -p output_Data\n"
                     f"Prepare_Methylation_Data.R "
                     f"https://tcga.xenahubs.net/download/TCGA."
                     f"{cancerType}.sampleMap/HumanMethylation450.gz /output_Data/TCGA_{cancerType}.tsv\n")
