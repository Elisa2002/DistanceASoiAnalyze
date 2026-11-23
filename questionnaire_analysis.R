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
library(car)


#data has valence in 4 lvls with 'all' added, need to remove 
#group by valence or condition for main effects and both for interaction 
#group by participant for per participant average - shapiro and outliers

#read data fill
anova_format_data_all <- read.csv(file="./figures/anova_data_format_2.csv",head=TRUE,sep=",")
anova_format_data_all
#----------------------------------------------------------------
#REMOVE all condition
anova_format_data <- anova_format_data_all[anova_format_data_all$valence != "all", ]
anova_format_data

#Only all condition
anova_just_all <- anova_format_data_all[anova_format_data_all$valence == "all",]
anova_just_all

q_data <- read.csv(file="./questionnaire_data.csv", head=TRUE, sep=";")
colnames(q_data) <- q_data[1,] #setting col names to row 1 contents
q_data <- q_data[-1,] #removing row 1 which is now duplicated with the col names
row.names(q_data) <- NULL #reset index
q_data[, -1] <- lapply(q_data[, -1], as.numeric) #data was considered string so now is considered numeric apart from participant number
q_data <- rename(q_data, "participant" = Participants)

q_data

#--------------------------------------------------------------------------------
#Create df for summary stats per variable 

summary_stat_df <- data.frame()

#---------------------------------------------------------------------------------
#visualize box plots for the variables of interest 
#table with full summary stats for variable I think are relevant for phase 2 results
summary_stats_table <- q_data %>%
  get_summary_stats(`MMSQ`, `CSQ_VR_Phase_2`, STAI_B, `STAI_A_Phase_2`, Isaac, Corsi, VVIQ, TSCS_Total,  type = "full")
summary_stats_table

summary_stats_table <- flextable(summary_stats_table)%>%
  #merge_v(j = "condition") %>%   # merge identical condition cells vertically
  #valign(j = "condition", valign = "top") %>%  # optional: align nicely
  theme_booktabs()
summary_stats_table <- set_caption(summary_stats_table, "Summary Statistics")
summary_stats_table


#boxplot creation template to visualise any
bxp <- ggboxplot(
  q_data, 
  y = "CSQ_VR_Phase_2")
bxp

#-------------------------------------------------------------------------------
#Prep for stats comparing the questionnaire variables to the memory tests and embodiment
#merge two data frames w q data second 
merged_df <- merge(anova_format_data, q_data, "participant")
#remove X col that appears after merge 
merged_df <- merged_df %>%
  subset(select = -X)

#covariation
#scatterplot code for corrected hits per avatar against any chosen questionnaire variable

me_data = merged_df[merged_df$condition== 'me',]#selecting data for me condition for visualisation purposes 

ggscatter(
  data = merged_df, x = "TSCS_Total", y = "corrected.hits", color = "condition", palette = "jco",
  add = "reg.line"
)+
  geom_jitter(aes(color = condition), position = position_jitter(width = .1))+
  stat_regline_equation(aes(label = after_stat(rr.label), color = condition))
                        

#ASSUMPTIONS
#independence of variables 
anova_model <- aov(CSQ_VR_Phase_2 ~ condition + valence, data = merged_df)
summary(anova_model)

#Levene test for homogeneity of variance
leveneTest(corrected.hits~condition, data = merged_df)
#ancova regression model with one of the questionnaires and condition taken into account in the model as to their effect on memory
#including any of the questionnaires does not seem to make the effect of condition on hits non significant 
Model5 <- lm(corrected.hits ~ condition + valence + CSQ_VR_Phase_2, data = merged_df)
summary(Model5)

#OTHER WAY TO DO ANCOVA
ancova_model <- aov(corrected.hits ~ condition + valence + CSQ_VR_Phase_2, data = merged_df)
Anova(ancova_model, type="III")