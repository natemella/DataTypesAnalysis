library(tidyverse)

### download data set

args <- commandArgs(trailingOnly = TRUE)


df2 <- read_tsv(args[1]) %>%
  mutate(Algorithm = str_replace(Algorithm, "_","\n")) %>%
  mutate(CancerType = str_replace(CancerType, "^TCGA_", ""), Algorithm=factor(Algorithm)) %>%
  group_by(Algorithm, CancerType, Description) %>%
  summarize(AUROC=mean(AUROC))

df2 = df2 %>%
  rename("Data_Type" = Description) %>%
  group_by(Algorithm, Data_Type) %>%
  summarise(AUROC=mean(AUROC))


cbPalette <- c("#8c510a", "#d8b365", "#f6e8c3", "gray50", "#c7eae5", "#5ab4ac", "#01665e", "#bcbd22")
df2 = mutate(df2, Data_Type = str_replace(Data_Type, "_","\n"))
df2 = mutate(df2, Data_Type = str_replace(Data_Type, "Expression","mRNA"))
df2 = mutate(df2, Data_Type = str_replace(Data_Type, "Methylation","Methyl"))



df2 %>%
  ggplot(aes(x = Data_Type, y = AUROC, color = Algorithm, shape = Algorithm)) +
  # scale_y_reverse() +
  theme_bw() +
  geom_jitter() +
  scale_shape_manual(values=c(3,4,7,8,11,15,17,18,19,6)) +
  coord_flip() +
  facet_grid(rows = vars(Data_Type), scales='free') +
  scale_color_manual(values = cbPalette) +
  xlab("Data Types") +
  theme(axis.text.y = element_blank(), axis.ticks.y = element_blank())

ggsave("../Graphs/data_type_facets.png", height = 7, width =7, dpi = 300)
