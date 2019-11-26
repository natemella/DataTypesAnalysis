

library(tidyverse)

## gets file name to be read in
args <- commandArgs(trailingOnly = TRUE)

df2 <- read_tsv(args[1]) %>%
  mutate(CancerType = str_replace(CancerType, "^TCGA_", ""), Algorithm=factor(Algorithm)) %>%
  group_by(Algorithm, CancerType, Description, Iteration) %>% summarize(AUROC=mean(AUROC)) %>%
  group_by(Algorithm, CancerType, Description) %>% summarize(AUROC=mean(AUROC)) %>%
  group_by(Algorithm, CancerType) %>% summarize(AUROC=max(AUROC))




# df3 <- df2 %>% group_by(CancerType, Description) %>% summarize(AUROC = max(AUROC)) %>% inner_join(df2, by = c("AUROC", "CancerType", "Description"))

cbPalette <- c("#8c510a", "#d8b365", "#f6e8c3", "gray50", "#c7eae5", "#5ab4ac", "#01665e", "black")
df2 %>%
  ggplot(aes(x = Algorithm, y = AUROC, color = Algorithm, shape = Algorithm)) +
  theme_bw(base_size=18) +
  scale_shape_manual(values=c(3,4,7,8,11,15,17,18,19,6)) +
  geom_jitter() +
  scale_y_continuous(breaks = scales::pretty_breaks(n = 10)) +
  coord_flip() +
  geom_hline(yintercept = 0.5, color = "red", linetype = "dashed") +
  facet_grid(rows = vars(CancerType)) +
  scale_color_manual(values = cbPalette) +
  xlab("") +
  # labs(color = "Data Type") +
  # ylim(0.15, 0.9) +
  theme(axis.text.y = element_blank(), axis.ticks.y = element_blank())

ggsave("../Graphs/cancer_type_max.png", height = 6, width = 10, dpi = 300)


