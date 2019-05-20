##install.packages("devtools")
##devtools::install_github("r-lib/xml2")
##install.packages("tidyverse")
library(tidyverse)
library(ggplot2)
library(stringr)

## gets file name to be read in
args <- commandArgs(trailingOnly = TRUE)

### reads in the file to be graphed
dataToBeGraphed <- read.table(args[1], header = TRUE)

### assigns the dataToBeGraphed to "x"
x <- dataToBeGraphed

### "y" is assinged the file name for naming the graph
y <- args[1]
y <- substr(y, 1, nchar(y)-4) 

### makes a new column that is the combination of CancerType and Algorithm
x$CancerType_Algorithm <- paste(x$CancerType,x$Algorithm,sep = "_")

### makes the table include only those four columns
### also, takes the mean of AUROC and condenses the table to only include the mean of AUROC
x <- aggregate(AUROC ~ CancerType_Algorithm + CancerType + Algorithm, x, mean)

#The Color blind friendly palette with black
cbPalette <- c("#999999", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7")

#change fills default color palette
scale_fill_manual(values = cbPalette)

### Makes the graph
myPlot <- ggplot(data = x) + geom_col(aes(x = Algorithm, y = AUROC, fill = Algorithm)) + ggtitle(y) + 
  theme(axis.text.x = element_text(angle = 56.5, hjust = 1, vjust = 1, size = 12)) + 
  theme(plot.title = element_text(hjust = .5, size = 20)) +theme(plot.margin=unit(c(1,1,1.5,2),"cm")) + 
  facet_wrap(~CancerType, nrow = 2)

### save the plot to folder "graphs" (a new folder created in wd)
y <- paste(y, "_barGraph.pdf", sep = "")
y <- paste("graphs/", y, sep = "")
pdf(y)
plot(myPlot)
dev.off()
print(y)

