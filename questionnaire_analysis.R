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
anova_format_data_all <- read.csv(file="~/Documents/cog_sup/M2_Internship/data_analysis/figures/anova_data_format_2.csv",head=TRUE,sep=",")
anova_format_data_all
#----------------------------------------------------------------
#REMOVE all condition
anova_format_data <- anova_format_data_all[anova_format_data_all$valence != "all", ]
anova_format_data

#Only all condition
anova_just_all <- anova_format_data_all[anova_format_data_all$valence == "all",]
anova_just_all

q_data <- read.csv(file="~/Documents/cog_sup/M2_Internship/data_analysis/questionnaire_data.csv", head=TRUE, sep=";")
colnames(q_data) <- q_data[1,] #setting col names to row 1 contents
q_data <- q_data[-1,] #removing row 1 which is now duplicated with the col names
row.names(q_data) <- NULL #reset index
q_data[, -1] <- lapply(q_data[, -1], as.numeric) #data was considered string so now is considered numeric apart from participant number
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

#boxplot creation template to visualise any
bxp <- ggboxplot(
  q_data, 
  y = "CSQ_VR_Phase_2")
bxp

#-------------------------------------------------------------------------------
#Prep for stats comparing the questionnaire variables to the memory tests and embodiment
