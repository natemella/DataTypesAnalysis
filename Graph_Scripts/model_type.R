

### load r packages


library(tidyverse)
library(readr)


### download data set

args <- commandArgs(trailingOnly = TRUE)

df <- read_tsv(args[1])


### average AUROC grouped by cancer type, algorithm and description(data type)


dfmean = df %>% group_by(CancerType, Algorithm, Description) %>% summarise(AUROC = mean(AUROC))


### assign ranks to each algorithm grouped by cancer type and description(data type)


dfranked = dfmean %>% group_by(CancerType, Description) %>% mutate(rank = rank(-AUROC)) %>% arrange(CancerType, Algorithm, rank)


### find the average across all cancer types grouped by description(data type) and algorithm


dfAveragedRanks = dfranked %>% group_by(Description, Algorithm) %>% summarise(avg_alg_rank = mean(rank), min_rank = min(rank), max_rank = max(rank)) %>% arrange(Algorithm)

print(dfAveragedRanks)
### make and save plot


cbPalette <- c("#8c510a", "#d8b365", "#f6e8c3", "gray50", "#c7eae5", "#5ab4ac", "#01665e")
dfAveragedRanks %>%
  ggplot(aes(x = Description, y = avg_alg_rank, color = Description, fill = Description)) +
  scale_y_reverse() +
  theme_bw() +
  geom_jitter() +
  # geom_linerange(ymin = dfAveragedRanks$max_rank, ymax = dfAveragedRanks$min_rank) +
  coord_flip() +
  facet_grid(rows = vars(Algorithm), scales='free') +
  scale_color_manual(values = cbPalette) +
  theme(axis.text.y = element_blank(), axis.ticks.y = element_blank())

ggsave("../Graphs/algorithm_fact.png", height = 7, width = 10, dpi = 300)
