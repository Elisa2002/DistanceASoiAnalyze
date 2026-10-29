library(tidyverse)
library(ggpubr)
library(dplyr) 
library(rstatix)
library(tibble)
library(flextable)
library(readxl)
library(lme4)
library(lmerTest)
library(mediation)
library(brms)


#data has valence in 4 lvls with 'all' added, need to remove 
#group by valence or condition for main effects and both for interaction 
#group by participant for per participant average - shapiro and outliers

#read data fill
anova_format_data_all <- read.csv(file="~/Documents/cog_sup/M2 Internship/data_analysis/figures/anova_data_format_2.csv",head=TRUE,sep=",")
anova_format_data_all
#----------------------------------------------------------------
#REMOVE all condition
anova_format_data <- anova_format_data_all[anova_format_data_all$valence != "all", ]
anova_format_data

#Only all condition
anova_just_all <- anova_format_data_all[anova_format_data_all$valence == "all",]
anova_just_all

#-----------------------------------------------------------------
#summary stats
table <- anova_format_data_all %>%
  group_by(valence) %>%
  get_summary_stats(source.errors.to.avatars, type = "mean_sd")%>%
  #mutate(condition = factor(condition, levels = c("me", "friend", "other", "robot")))%>%
  arrange(valence)
table
table <- flextable(table)%>%
  #merge_v(j = "condition") %>%   # merge identical condition cells vertically
  #valign(j = "condition", valign = "top") %>%  # optional: align nicely
  theme_booktabs()
table <- set_caption(table, "Summary Statistics - Corrected Item Hit Rate per Valence")
table

#summary stats
table <- anova_format_data_all %>%
  group_by(condition, valence) %>%
  get_summary_stats(source.errors.to.avatars, type = "mean_sd")%>%
  mutate(condition = factor(condition, levels = c("me", "friend", "other", "robot")))%>%
  arrange(condition, valence)
table
table <- flextable(table)%>%
  merge_v(j = "condition") %>%   # merge identical condition cells vertically
  valign(j = "condition", valign = "top") %>%  # optional: align nicely
  theme_booktabs()
table <- set_caption(table, "Summary Statistics - Corrected Item Hit Rate per Valence per Condition")
table

anova_format_data_all %>%
  group_by(condition, valence) %>%
  get_summary_stats(source.hits, type = "mean_sd")

anova_format_data %>%
  group_by(condition) %>%
  get_summary_stats(source.errors.to.avatars, type = "mean_sd")

anova_just_all %>%
  group_by(condition) %>%
  get_summary_stats(source.errors.to.avatars, type = "mean_sd")

#boxplot for corrected hits to visualize per condition and valence
hits_bxp <- ggboxplot(
  anova_format_data_all, 
  x = "condition", 
  y = "corrected.hits", 
  color = "valence",
  palette = 'jco')

hits_bxp

#boxplot not per condition
hits_bxp <- ggboxplot(
  anova_format_data_all, 
  y = "corrected.hits",
  palette = 'jco')

hits_bxp

#boxplot not per condition
hits_bxp <- ggboxplot(
  anova_format_data_all, 
  y = "source.hits",
  palette = 'jco')

hits_bxp

hits_bxp <- ggboxplot(
  anova_format_data, 
  y = "source.errors.to.avatars",
  palette = 'jco')

hits_bxp

#same boxplot but for source hits
source_bxp <- ggboxplot(
  anova_format_data_all,
  x = 'condition',
  y = 'source.hits',
  color = 'valence',
  palette = "jco"
)
source_bxp

#OUTLIERS -------------------------------------------------------
#outliers per condition and valence for hits item
anova_format_data %>%
  identify_outliers(corrected.hits)

#outliers for source hits
anova_format_data %>%
  identify_outliers(source.hits)

anova_format_data %>%
  identify_outliers(source.errors.to.avatars)

#NORMALITY -----------------------------------------------------
#SHAPIRO test for normality
#to be done for each anova 
#need bigger 0.05 p val

ch_shapiro <- anova_just_all %>%
  group_by(valence) %>%
  shapiro_test(corrected.hits)
ggqqplot(anova_just_all, "corrected.hits", ggtheme = theme_bw())

ch_shapiro <- flextable(ch_shapiro)%>%
  theme_booktabs()
ch_shapiro <- set_caption(ch_shapiro, "Shapiro-Wilks Normality Test Corrected Hits")
ch_shapiro

sh_shapiro <-anova_just_all %>%
  group_by(valence) %>%
  shapiro_test(source.hits)
ggqqplot(anova_just_all, "source.hits", ggtheme = theme_bw())

sh_shapiro <- flextable(sh_shapiro)
sh_shapiro <- set_caption(sh_shapiro, "Shapiro-Wilks Normality Test Source Hits")
sh_shapiro

anova_just_all %>%
  group_by(valence) %>%
  shapiro_test(hits..uncorrected.)
ggqqplot(anova_just_all, "hits..uncorrected.", ggtheme = theme_bw())

fa_shapiro <- anova_just_all %>%
  group_by(valence)%>%
  shapiro_test(false.alarms)
ggqqplot(anova_just_all, "false.alarms", ggtheme = theme_bw())

fa_shapiro <- flextable(fa_shapiro)%>%
  theme_booktabs()
fa_shapiro <- set_caption(fa_shapiro, "Shapiro-Wilks Normality Test False Alarms")
fa_shapiro

miss_shapiro <- anova_just_all %>%
  group_by(valence) %>%
  shapiro_test(misses)
miss_shapiro<- flextable(miss_shapiro)
miss_shapiro <- set_caption(miss_shapiro, "Shapiro-Wilks Normallity Test Misses")
miss_shapiro
ggqqplot(anova_just_all, "misses", ggtheme = theme_bw())

se_shapiro <- anova_just_all %>%
  group_by(valence) %>%
  shapiro_test(source.errors.to.avatars)
se_shapiro <-flextable(se_shapiro)
se_shapiro <- set_caption(se_shapiro, "Shapiro-Wilks Normality Test Source Errors")
se_shapiro
ggqqplot(anova_just_all, "source.errors.to.avatars", ggtheme = theme_bw())

em_shapiro <- anova_just_all %>%
  group_by(valence) %>%
  shapiro_test(merged_em_score)
em_shapiro <- flextable(em_shapiro)
em_shapiro <- set_caption(em_shapiro, "Shapiro-Wilks Normality Test Embodiment")
em_shapiro
ggqqplot(anova_just_all, "merged_em_score", ggtheme = theme_bw())

adj_shapiro <- 
  anova_just_all %>%
  group_by(valence) %>%
  shapiro_test(number_of_adj_per_avatar)
adj_shapiro <- flextable(adj_shapiro)
adj_shapiro <- set_caption(adj_shapiro, "Shapiro-Wilks Normality Test Number of Adjectives per Avatar")
adj_shapiro
ggqqplot(anova_just_all, "number_of_adj_per_avatar", ggtheme = theme_bw())

#plot shows distribution  
ggqqplot(anova_format_data_all, "corrected.hits", ggtheme = theme_bw()) +
  facet_grid(condition ~ valence, labeller = "label_both")

#ANOVA----------------------------------------------------------------
#ANOVAS - one for each variable total 7 

# APA FORMATTING FUNCTIONS ---------------------------------------------

apa_anova <- function(anova_object, caption_text){
  
  get_anova_table(anova_object) %>%
    as_tibble() %>%
    rename(`η²ₚ` = pes) %>%
    mutate(
      F = round(F, 2),
      DFn = round(DFn, 0),
      DFd = round(DFd, 0),
      `η²ₚ` = round(`η²ₚ`, 3),
      p = p_format(p)
    ) %>%
    flextable() %>%
    set_caption(caption_text)
  
}


apa_posthoc <- function(data, formula_text, caption_text){
  
  pairwise_t_test(
    data = data,
    formula = formula_text,
    paired = TRUE,
    p.adjust.method = "bonferroni"
  ) %>%
    as_tibble() %>%
    mutate(
      statistic = round(statistic, 2),
      p = p_format(p),
      p.adj = p_format(p.adj)
    ) %>%
    flextable() %>%
    set_caption(caption_text)
  
}

#valence x condition on item HITS CORRECTED
res.aov_hits <- anova_test(
  data = anova_format_data,
  dv = corrected.hits,
  wid = participant,
  within = c(condition, valence),
  effect.size = "pes"
)

apa_anova(
  res.aov_hits,
  "Two-Way Repeated-Measures ANOVA: Corrected Hit Rate"
)

#POST HOC
# comparisons for condition variable
apa_posthoc(
  anova_format_data,
  corrected.hits ~ condition,
  "Pairwise Comparisons for Main Effect of Condition on Corrected Hits"
)

apa_posthoc(
  anova_format_data,
  corrected.hits ~ valence,
  "Pairwise Comparisons for Main Effect of Valence on Corrected Hits"
)
#UNCORRECTED
res.aov_hits_uncorrected <- anova_test(
  data = anova_format_data, dv = hits..uncorrected., wid = participant,
  within = c(condition, valence)
)
get_anova_table(res.aov_hits_uncorrected)

#SOURCE HITS
res.aov_source <- anova_test(
  data = anova_format_data,
  dv = source.hits,
  wid = participant,
  within = c(condition, valence),
  effect.size = "pes"
)

apa_anova(
  res.aov_source,
  "Two-Way Repeated-Measures ANOVA: Source Hits"
)

res.aov_source_o <- anova_test(
  data = anova_format_data,
  dv = o.source.hits,
  wid = participant,
  within = c(condition, valence),
  effect.size = "pes"
)

apa_anova(
  res.aov_source_o,
  "Two-Way Repeated-Measures ANOVA: Reviewed Source Hits"
)
#POST HOC
# comparisons for condition main and valence main
apa_posthoc(
  anova_format_data,
  source.hits ~ condition,
  "Pairwise Comparisons for Condition on Source Hits"
)

apa_posthoc(
  anova_format_data,
  source.hits ~ valence,
  "Pairwise Comparisons for Valence on Source Hits"
)

apa_posthoc(
  anova_format_data,
  o.source.hits ~ condition,
  "Pairwise Comparisons for Condition on Reviewed Source Hits"
)

apa_posthoc(
  anova_format_data,
  o.source.hits ~ valence,
  "Pairwise Comparisons for Valence on Reviewed Source Hits"
)

#MISSES
res.aov_miss <- anova_test(
  data = anova_format_data,
  dv = misses,
  wid = participant,
  within = c(condition, valence),
  effect.size = "pes"
)

apa_anova(
  res.aov_miss,
  "Two-Way Repeated-Measures ANOVA: Misses"
)
#POST HOC
# comparisons for condition variable
apa_posthoc(
  anova_format_data,
  misses ~ condition,
  "Pairwise Comparisons for Main Effect of Condition on Misses"
)

apa_posthoc(
  anova_format_data,
  misses ~ valence,
  "Pairwise Comparisons for Main Effect of Valence on Misses"
)

#FALSE ALARMS
res.aov_fa <- anova_test(
  data = anova_just_all,
  dv = false.alarms,
  wid = participant,
  within = condition,
  effect.size = "pes"
)

apa_anova(
  res.aov_fa,
  "One-Way Repeated-Measures ANOVA: False Alarms"
)
#SOURCE ERRORS
res.aov_source_errors <- anova_test(
  data = anova_format_data,
  dv = source.errors.to.avatars,
  wid = participant,
  within = c(condition, valence),
  effect.size = "pes"
)

apa_anova(
  res.aov_source_errors,
  "Two-Way Repeated-Measures ANOVA: Source Errors"
)
#POST HOC
# comparisons for condition
apa_posthoc(
  anova_format_data,
  source.errors.to.avatars ~ condition,
  "Pairwise Comparisons for Main Effect of Condition on Source Errors"
)

#NUMBER of words per avatar per valence 
res.aov_adj_num <- anova_test(
  data = anova_format_data,
  dv = number_of_adj_per_avatar,
  wid = participant,
  within = c(condition, valence),
  effect.size = "pes"
)

apa_anova(
  res.aov_adj_num,
  "Two-Way Repeated-Measures ANOVA: Number of Adjectives Attributed to Avatars"
)
#POST HOC - main effect
# main effect valence
apa_posthoc(
  anova_format_data,
  number_of_adj_per_avatar ~ valence,
  "Pairwise Comparisons for Main Effect of Valence on Number of Adjectives Selected"
)

#main effect conditon
# main effect valence
apa_posthoc(
  anova_format_data,
  number_of_adj_per_avatar ~ condition,
  "Pairwise Comparisons for Main Effect of Condition on Number of Adjectives Selected"
)

#interaction effect valence condition
# Effect of condition at each valence
one.way <- anova_format_data %>%
  group_by(valence) %>%
  anova_test(
    dv = number_of_adj_per_avatar,
    wid = participant,
    within = condition,
    effect.size = "pes"
  ) %>%
  get_anova_table() %>%
  as_tibble() %>%
  rename(`η²ₚ` = pes) %>%
  mutate(
    F = round(F, 2),
    DFn = round(DFn, 0),
    DFd = round(DFd, 0),
    `η²ₚ` = round(`η²ₚ`, 3),
    p = p_format(p)
  ) %>%
  flextable() %>%
  set_caption(
    "Simple Effects Repeated-Measures ANOVAs: Effect of Condition Within Each Valence"
  )

one.way

# Pairwise comparisons between conditions

pwc <- anova_format_data %>%
  group_by(valence) %>%
  pairwise_t_test(
    number_of_adj_per_avatar ~ condition,
    paired = TRUE,
    p.adjust.method = "bonferroni"
  ) %>%
  as_tibble() %>%
  mutate(
    statistic = round(statistic, 2),
    p = p_format(p),
    p.adj = p_format(p.adj)
  ) %>%
  flextable() %>%
  set_caption(
    "Pairwise Comparisons Between Conditions Within Each Valence"
  )

pwc

#avatar effect on EMBODIMENT - embodiment is not separate per valence
anova_data_for_em <- anova_format_data %>%
  group_by(participant, condition) %>%
  summarise(merged_em_score = mean(merged_em_score),
            .groups = "drop")

res.aov_adj_em <- anova_test(
  data = anova_data_for_em,
  dv = merged_em_score,
  wid = participant,
  within = condition,
  effect.size = "pes"
)

apa_anova(
  res.aov_adj_em,
  "One-Way Repeated-Measures ANOVA: Embodiment Score"
)
# pairwise comparisons

apa_posthoc(
  anova_data_for_em,
  merged_em_score ~ condition,
  "Pairwise Comparisons for Main Effect of Condition on Embodiment Scores"
)

#INCLUSION SELF OTHER 
res.aov_relation <- anova_test(
  data = anova_just_all,
  dv = relation_image,
  wid = participant,
  within = condition,
  effect.size = "pes"
)

apa_anova(
  res.aov_relation,
  "One-Way Repeated-Measures ANOVA: Perceived Distance to Self"
)

apa_posthoc(
  anova_just_all,
  relation_image ~ condition,
  "Pairwise Comparisons for Main Effect of Condition on Percieved Distance to Self"
)

my_comparisons <- list(c("me", "friend"), c("me", "other"), c("me", "robot"), c("friend", "other"), c("friend", "robot"), c("other", "robot"))
avatars <- c("me", "friend", "other", "robot")

ggplot(anova_just_all,  aes(x = factor(condition, avatars), y = relation_image, fill = factor(condition, avatars))) +
  geom_boxplot(outlier.shape = NA)+
  theme_minimal() +
  labs(title="Percieved Closeness to Each Avatar", 
       x="Avatar at Encoding", y = "Proximity to Avatar")+ 
  ylim(0, 7)+
  scale_fill_brewer(palette = "Set2")+
  theme(legend.position = "none")

#-----------------------------------------------------------------------
#PLOTTING
#Corrected hits 
#condition
my_comparisons <- list(c("me", "friend"), c("me", "other"), c("me", "robot"), c("friend", "other"), c("friend", "robot"), c("other", "robot"))
avatars <- c("me", "friend", "other", "robot")
ggplot(anova_format_data, aes(x = factor(condition, avatars), y = corrected.hits)) +
  geom_bar(stat="summary", fun="mean", width=0.5, alpha=0.7) +
  geom_errorbar(stat="summary", fun.data = mean_se, width=0.4) +
  stat_compare_means(comparisons = my_comparisons, label = "p.signif", label.y = c(0.80, 0.90, 0.95, 0.75, 0.85, 0.80)) +
  theme_minimal() +
  labs(title="Average Corrected Hit Rate per Avatar Condition", 
       x="Avatar at Encoding", y = "Mean Corrected Hit Rate")+ 
  ylim(0, 1)

ggplot(anova_format_data,  aes(x = factor(condition, avatars), y = corrected.hits, fill = factor(condition, avatars))) +
  geom_boxplot(outlier.shape = NA)+
  
  stat_compare_means(comparisons = my_comparisons, label = "p.signif", label.y = c(1.10, 1.30, 1.40, 1.10, 1.20, 1.10)) +
  theme_minimal() +
  labs(title="Average Corrected Hit Rate per Avatar Condition", 
       x="Avatar at Encoding", y = "Mean Corrected Hit Rate")+ 
  ylim(0, 1.5)+
  scale_fill_brewer(palette = "Set2")+
  theme(legend.position = "none")

#valence
comparison_val <- list(c("pos", "neut"), c("neut", "neg"), c("pos", "neg"))
valence_order <- c("pos", "neut", "neg")
ggplot(anova_format_data, aes(x = factor(valence, valence_order), y = corrected.hits)) +
  geom_bar(stat="summary", fun="mean", width=0.5, alpha=0.7) +
  geom_errorbar(stat="summary", fun.data = mean_se, width=0.4) +
  stat_compare_means(comparisons = comparison_val, label = "p.signif", label.y = c(0.75, 0.80, 0.95)) +
  theme_minimal() +
  labs(title="Average Corrected Hit Rate per Adjective Valence", 
       x="Adjective Valence at Encoding", y = "Mean Corrected Hit Rate")+ 
  ylim(0, 1)

ggplot(anova_format_data,  aes(x = factor(valence, valence_order), 
                               y = corrected.hits,
                               fill = factor(valence, valence_order))) +
  geom_boxplot(outlier.shape = NA)+
  
  stat_compare_means(comparisons = comparison_val, 
                     label = "p.signif",
                     label.y = c(1.2, 1.2, 1)) +
  theme_minimal() +
  labs(title="Average Corrected Hit Rate per Adjective Valence", 
       x="Adjective Valence at Encoding", y = "Mean Corrected Hit Rate")+ 
  ylim(0, 1.3)+
  scale_fill_brewer(palette = "Paired")+
  theme(legend.position = "none")

#False Alarms

#Misses
ggplot(anova_format_data, aes(x = factor(condition, avatars), y = misses)) +
  geom_bar(stat="summary", fun="mean", width=0.5, alpha=0.7) +
  geom_errorbar(stat="summary", fun.data = mean_se, width=0.4) +
  #stat_compare_means(comparisons = my_comparisons, label = "p.signif", label.y = c(0.65, 0.70, 0.90, 0.60, 0.80, 0.65)) +
  theme_minimal() +
  labs(title="Average Miss Rate per Avatar Condition", 
       x="Avatar at Encoding", y = "Mean Miss Rate")+ 
  ylim(0, 1)

#Source hits
ggplot(anova_format_data, aes(x = factor(condition, avatars), y = source.hits)) +
  geom_bar(stat="summary", fun="mean", width=0.5, alpha=0.7) +
  geom_errorbar(stat="summary", fun.data = mean_se, width=0.4) +
  stat_compare_means(comparisons = my_comparisons, label = "p.signif", label.y = c(0.65, 0.70, 0.90, 0.60, 0.80, 0.65)) +
  theme_minimal() +
  labs(title="Average Source Hit Rate per Avatar Condition", 
       x="Avatar at Encoding", y = "Mean Source Hit Rate")+ 
  ylim(0, 1)

ggplot(anova_format_data,  aes(x = factor(condition, avatars), y = source.hits, fill = factor(condition, avatars))) +
  geom_boxplot(outlier.shape = NA)+
  
  stat_compare_means(comparisons = my_comparisons, label = "p.signif", label.y = c(1.10, 1.30, 1.40, 1.10, 1.20, 1.10)) +
  theme_minimal() +
  labs(title="Average Source Hit Rate per Avatar Condition", 
       x="Avatar at Encoding", y = "Mean Source Hit Rate")+ 
  ylim(0, 1.5)+
  scale_fill_brewer(palette = "Set2")+
  theme(legend.position = "none")


#valence
ggplot(anova_format_data, aes(x = factor(valence, valence_order), y = source.hits)) +
  geom_bar(stat="summary", fun="mean", width=0.5, alpha=0.7) +
  geom_errorbar(stat="summary", fun.data = mean_se, width=0.4) +
  stat_compare_means(comparisons = comparison_val, label = "p.signif", label.y = c(0.75, 0.80, 0.95)) +
  theme_minimal() +
  labs(title="Average Corrected Hit Rate per Adjective Valence", 
       x="Adjective Valence at Encoding", y = "Mean Corrected Hit Rate")+ 
  ylim(0, 1)

ggplot(anova_format_data, aes(x = factor(valence, valence_order), y = source.hits)) +
  geom_bar(stat="summary", fun="mean", width=0.5, alpha=0.7) +
  geom_errorbar(stat="summary", fun.data = mean_se, width=0.4) +
  stat_compare_means(comparisons = comparison_val, label = "p.signif", label.y = c(0.75, 0.80, 0.95)) +
  theme_minimal() +
  labs(title="Average Corrected Hit Rate per Adjective Valence", 
       x="Adjective Valence at Encoding", y = "Mean Corrected Hit Rate")+ 
  ylim(0, 1)


ggplot(anova_format_data,  aes(x = factor(valence, valence_order), 
                               y = source.hits,
                               fill = factor(valence, valence_order))) +
  geom_boxplot(outlier.shape = NA)+
  
  theme_minimal() +
  labs(title="Average Source Hit Rate per Adjective Valence", 
       x="Adjective Valence at Encoding", y = "Mean Source Hit Rate")+ 
  ylim(0, 1)+
  scale_fill_brewer(palette = "Paired")+
  theme(legend.position = "none")



#Source errors
ggplot(anova_format_data, aes(x = factor(condition, avatars), y = source.errors.to.avatars)) +
  geom_bar(stat="summary", fun="mean", width=0.5, alpha=0.7) +
  geom_errorbar(stat="summary", fun.data = mean_se, width=0.4) +
  #stat_compare_means(
  #  comparisons = my_comparisons,
  #  method = "t.test",
  #  paired = TRUE,
  #  p.adjust.method = "bonferroni",
  #  label = "p.signif",
  #  label.y = c(0.25, 0.30, 0.50, 0.25, 0.40, 0.25)
  #)+
  theme_minimal() +
  labs(title="Average Proportion of Source Errors Towards Each Avatar", 
       x="Avatar Recalled", y = "Mean Source Error")+ 
  ylim(0, 1)

my_comparisons_fixed <- list(c("me", "friend"), c("me", "other"), c("friend", "other"), c("friend", "robot"), c("other", "robot"))
ggplot(anova_just_all,  aes(x = factor(condition, avatars), 
                               y = source.errors.to.avatars,
                               fill = factor(condition, avatars))) +
  geom_boxplot(outlier.shape = NA)+
  
  stat_compare_means(comparisons = my_comparisons, 
                     label = "p.signif",
                     label.y = c(0.14, 0.15,0.2,0.14,0.18, 0.17)) +
  # manually add the corrected significance marker
  #annotate("text",
  #         x = 2.5,          # midpoint between groups
  #         y = 0.19,
  #         label = "ns",      # or "**", "***", "ns"
  #         size = 4) +'''
  
  # optional bracket
  #annotate("segment", x = 1, xend = 4, y = 0.18, yend = 0.18, linewidth = 0.3)+
  
  theme_minimal() +
  labs(title="Average Proportion of Source Errors Towards Each Avatar", 
       x="Avatar Recalled", y = "Mean Source Error Rate")+ 
  ylim(0, 0.5)+
  scale_fill_brewer(palette = "Set2")+
  theme(legend.position = "none")

#Adjectives per avatar 
ggbarplot(
  anova_format_data,
  x = "valence",
  y = "number_of_adj_per_avatar",
  fill = "condition",
  position = position_dodge(0.8),
  add = "mean_se",
  error.plot = "errorbar"
) +
  geom_signif(
    annotations = "**",
    y_position = 4.8,
    xmin = 2.8,
    xmax =3.35
  ) +
  ylim(0, 6) +
  theme_minimal() +
  labs(
    title = "Number of Adjectives Selected Per Avatar",
    x = "Avatar Selected",
    y = "Average Number of Adjectives"
  )

ggline(anova_format_data, x = "valence", y = "number_of_adj_per_avatar", add = "mean_se",
       color = "condition", palette = "jco")+
  stat_compare_means(aes(group = condition), label = "p.signif", 
                     label.y = c(3,4,5,6,7,8,9))+ 
  ylim(0, 5)

ggplot(anova_format_data,  aes(x = factor(valence, valence_order), y = number_of_adj_per_avatar, color = condition)) +
  geom_boxplot()+
  stat_compare_means(comparisons = my_comparisons_val, label = "p.signif", label.y = c(1.10, 1.30, 1.40, 1.10, 1.20, 1.10)) +
  theme_minimal() +
  labs(title="Number of Adjectives Selected Per Avatar", 
       x="Avatar Selected", y = "Average Number of Adjectives")+
  ylim(0, 7)

ggplot(anova_format_data,  aes(x = factor(condition, avatars), y = relation_image, color = condition)) +
  geom_boxplot()+
  theme_minimal() +
  labs(title="Inclusion Self in Other", 
       x="Avatar", y = "Score of Inclusion Self in Other")+
  ylim(0, 7)



#Embodiment 
ggplot(anova_data_for_em, aes(x = factor(condition, avatars), y = merged_em_score, fill= condition)) +
  geom_bar(stat="summary", fun="mean", width=0.5, alpha=0.7) +
  geom_errorbar(stat="summary", fun.data = mean_se, width=0.4) +
  stat_compare_means(
    comparisons = my_comparisons,
    method = "t.test",
    paired = TRUE,
    p.adjust.method = "bonferroni",
    label = "p.signif",
  #label.y = c(0.25, 0.30, 0.50, 0.25, 0.40, 0.25)
  )+
  theme_minimal() +
  labs(title="Average Embodiment Scores per Avatar Condition", 
       x="Avatar Embodied", y = "Mean Embodiment Score")


#-------------------------------------------------------------------------
#EMBODIMENT AND CONDITION 

anova_just_all$condition <- factor(anova_just_all$condition, levels = c("friend", "me", "other", "robot"))

# Création des variables dummy (friend = référence)
# /!\ IMPORTANT : ces 3 lignes créent les colonnes binaires nécessaires à l'analyse.
# Chaque colonne vaut 1 si le participant est dans cette condition, 0 sinon.
# La condition "friend" sert de référence (quand les 3 sont à 0, c'est friend).
# Ne pas les supprimer même si la colonne "condition" existe déjà dans le CSV.
anova_just_all$cond_me    <- as.numeric(anova_just_all$condition == "me")
anova_just_all$cond_other <- as.numeric(anova_just_all$condition == "other")
anova_just_all$cond_robot <- as.numeric(anova_just_all$condition == "robot")

# CHEMIN A : condition → merged_em_score
#does contiion predict embodiment 

mod_a <- lmer(merged_em_score ~ cond_me + cond_other + cond_robot + (1 | participant),
              data = anova_just_all, REML = FALSE)
summary(mod_a)

# CHEMIN B + effet direct : merged_em_score + condition → corrected.hits
#does condition still affect hits after emodiment is taken into account 
# ============================================================
mod_b <- lmer(corrected.hits ~ merged_em_score + cond_me + cond_other + cond_robot + (1 | participant),
              data = anova_just_all, REML = FALSE)
summary(mod_b)

# ============================================================
# MÉDIATION BOOTSTRAPPÉE
# Une médiation séparée par condition (vs friend)
# ============================================================

set.seed(42)
n_boot <- 5000

# -- me vs friend --
med_me <- mediate(
  model.m = lmer(merged_em_score ~ cond_me + (1 | participant), data = anova_just_all , REML = FALSE),
  model.y = lmer(corrected.hits ~ merged_em_score + cond_me + (1 | participant), data = anova_just_all, REML = FALSE),
  treat = "cond_me",
  mediator = "merged_em_score",
  boot = FALSE,
  sims = n_boot
)
summary(med_me)hi

# -- other vs friend --
med_other <- mediate(
  model.m = lmer(merged_em_score ~ cond_other + (1 | participant), data = anova_just_all, REML = FALSE),
  model.y = lmer(corrected.hits ~ merged_em_score + cond_other + (1 | participant), data = anova_just_all, REML = FALSE),
  treat = "cond_other",
  mediator = "merged_em_score",
  boot = FALSE,
  sims = n_boot
)
summary(med_other)

# -- robot vs friend --
med_robot <- mediate(
  model.m = lmer(merged_em_score ~ cond_robot + (1 | participant), data = anova_just_all, REML = FALSE),
  model.y = lmer(corrected.hits ~ merged_em_score + cond_robot + (1 | participant), data = anova_just_all, REML = FALSE),
  treat = "cond_robot",
  mediator = "merged_em_score",
  boot = FALSE,
  sims = n_boot
)
summary(med_robot)

