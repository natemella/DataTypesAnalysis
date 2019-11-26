library(dplyr)
library(tidyverse)
library(readxl)


myList = c("BLCA", "BRCA", "HNSC", "KIRC", "LGG", "LUAD", "PRAD", "STAD", "THCA", "UCEC")
### download data set
df <- read_excel("1-s2.0-S0092867418302290-mmc1.xlsx", sheet=1)

df <- df[df$type %in% myList,]



completeFun <- function(data, desiredCols) {
  completeVec <- complete.cases(data[, desiredCols])
  return(data[completeVec, ])
}

completeFun(df, "PFI.time")
df$PFI.time[which(is.na(df$PFI.time))] <- 0

l <- c()
for (value in myList) {
  a <-df[df$type %in% c(value),]
  b <- (mean(a$PFI.time) + 180)
  l <- c(l, b)
}
l2 <- c()
for (value in myList) {
  a <-df[df$type %in% c(value),]
  b <- (mean(a$PFI.time) - 180)
  l2 <- c(l2, b)
}

cbPalette <- c("#9ca5ac",  "#111e3e")

dat <- data.frame(x=rep(l), y=rep(l2), type=rep(myList))
vline.dat <- data.frame(type=levels(dat$type), l)



# df1<-merge(x=df, y=vline.dat, by="type", all= TRUE)


df %>%
  ggplot(aes(x = PFI.time)) +
  # facet_grid(rows = vars(type), scales='free') +
  theme_bw() +
  geom_histogram() +
  geom_vline(aes(xintercept=l), data=vline.dat, colour="pink") +
  geom_vline(aes(xintercept=l2), data=vline.dat, colour="blue") +
  facet_grid(rows = vars(type)) +
  scale_fill_manual(values = cbPalette)

ggsave("../Graphs/PFI.time.png", height = 7, width = 7, dpi = 300)
