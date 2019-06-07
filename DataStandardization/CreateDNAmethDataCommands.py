with open("CancerTypes.txt") as input:
    output = open("DNA_MethylationFiles.sh", "w")
    for line in input:
        line = line.strip("\n")
        output.write(f"mkdir -p output_Data\n"
                     f"docker run --rm \\\n"
                     f"-v `pwd`/output_Data:/output_Data \\\n"
                     f"-v `pwd`:/Scripts \\\n"
                     f"--user $(id -u):$(id -g) \\\n"
                     f"rocker/tidyverse Rscript /Scripts/Prepare_Methylation_Data.R "
                     f"https://tcga.xenahubs.net/download/TCGA."
                     f"{line}.sampleMap/HumanMethylation450.gz {line}\n")


