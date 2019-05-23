# You only need to install the packages once
#install.packages(c("readr", "dplyr", "tidyr", "stringr"))

library(readr)
library(dplyr)
library(tidyr)
library(stringr)

## Get command line args
args <- commandArgs(trailingOnly = TRUE)

## Read metadata
metadata <- read_tsv("GPL16304-47833.txt.gz", comment="#") %>%
  select(ID, Distance_closest_TSS, Closest_TSS_gene_name) %>%
  dplyr::rename(Probe=ID, TSS_Distance=Distance_closest_TSS, Gene=Closest_TSS_gene_name) %>%
  arrange(Gene, TSS_Distance)

## Read data
rawData <- read_tsv(args[1]) %>%
  dplyr::rename(Probe=sample)

# Merge and clean up the data
data <- inner_join(metadata, rawData, by="Probe")

# This frees some memory
rm(metadata)
rm(rawData)
#data <- data[1:10000,]

tidyData <- gather(data, Patient_ID, beta, -Probe, -TSS_Distance, -Gene, na.rm=TRUE)
tidyData$Patient_ID <- substring(tidyData$Patient_ID, 1, 12)

## Filter data to include only probes closest to TSS
maxTSSDistance <- 300
filteredData <- filter(tidyData, TSS_Distance > -maxTSSDistance) %>%
  filter(TSS_Distance < maxTSSDistance) %>%
  select(-TSS_Distance)

## Summarize to median value per gene (this should exclude outliers)
filteredData <- group_by(filteredData, Patient_ID, Gene) %>%
  summarise(Value=median(beta)) %>%
  ungroup()

## Put the data back into a "wide" format
filteredData <- spread(filteredData, Gene, Value)

## Save data to an output file
outPutFile <- paste("Methylation_Data_", args[2], ".txt", sep = "")
write_tsv(filteredData, outPutFile)