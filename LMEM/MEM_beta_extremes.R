library(data.table)
library(rstatix) # нет пакета в 3.6.3
library(ggplot2)
library(lme4)
library("ggpubr") # нет пакета в 3.6.3
library(emmeans)
library(lsmeans)
library(gridExtra)
library(lmerTest)


####### Minimums ##########
# Шаг1. Ищем p-value и коэффициент регрессии по полной модели (full LMEM)
# Возможен вариант Шага 1, когда используем обычную линейную регрессию для выбора сенсоров (lin_reg_beta.R)
# Построение модели для 102 сенсоров в цикле 
# Задаем пустые списки для коэффициентов корреляции и p_value
reg_coeff <- NULL
p_val <- NULL

# задаем список от 0 до 101

num <- 0:101
for(i in num){
  df <- read.csv(paste('active1_st_',as.character(i),'.csv',sep=''))
  ### превращаем нужные переменные в факторы ###
  df$stimulus <- factor(df$stimulus)
  df$subjects <- factor(df$subjects)
  
  # строим линейную модель со смешенными эффектами
  Model <- lmer(min_beta_PreM ~ RTs + (1 + RTs|subjects) + (1 + RTs|stimulus), data=df)
  
  # извлекаем необходимые значения из summary 
  Sum <- coef(summary(Model))
  x <- Sum[2,1]
  y <- Sum[2,5]
  reg_coeff <- c(reg_coeff,x)
  p_val <- c(p_val,y)
}

#смотрим полученные значения
#p_val

#создаем dataframe из полученных в цикле списков
dframe <- data.frame("reg_coeff" = reg_coeff, "p_val" = p_val)

#записываем полученный dataframe в csv файл
write.csv(dframe,"active1_st_minimums_PreM_full_LMEM.csv", row.names = FALSE)

####### Maximums ##########
# Шаг1. Ищем p-value и коэффициент регрессии по полной модели (full LMEM)
# Возможен вариант Шага 1, когда используем обычную линейную регрессию для выбора сенсоров (lin_reg_beta.R)
# Построение модели для 102 сенсоров в цикле 
# Задаем пустые списки для коэффициентов корреляции и p_value
reg_coeff <- NULL
p_val <- NULL

# задаем список от 0 до 101

num <- 0:101
for(i in num){
  df <- read.csv(paste('active1_st_',as.character(i),'.csv',sep=''))
  ### превращаем нужные переменные в факторы ###
  df$stimulus <- factor(df$stimulus)
  df$subjects <- factor(df$subjects)
  
  # строим линейную модель со смешенными эффектами
  Model <- lmer(max_beta_PostM ~ RTs + (1 + RTs|subjects) + (1 + RTs|stimulus), data=df)
  
  # извлекаем необходимые значения из summary 
  Sum <- coef(summary(Model))
  x <- Sum[2,1]
  y <- Sum[2,5]
  reg_coeff <- c(reg_coeff,x)
  p_val <- c(p_val,y)
}

#смотрим полученные значения
#p_val

#создаем dataframe из полученных в цикле списков
dframe <- data.frame("reg_coeff" = reg_coeff, "p_val" = p_val)

#записываем полученный dataframe в csv файл
write.csv(dframe,"active1_st_maximum_PostM_full_LMEM.csv", row.names = FALSE)


####################################################################################################
##################### Шаг 2. По выбраным сенсорам  ##############################################
#####################(наименьшее значение p value - алгоритм в search_significants_sensors.ipynb), 
#выбираем LMEM

########################### Active1 start Minimum PreM ##############################

#Для одного сенсора
df <- read.csv('active1_st_18.csv')
### превращаем нужные переменные в факторы ###
df$stimulus <- factor(df$stimulus)
df$subjects <- factor(df$subjects)

#строим модель
Model <- lmer(min_beta_PreM ~ RTs + (1 + RTs|subjects) + (1 + RTs|stimulus), data=df)
summary(Model)


s <- step(Model) #автоматически ищем упрощенную модель
s

#по сенсору выбранному с помощью full LMEM
#s - выдает предупрежедения и упрощенную модель 
#Model found:
# min_beta_PreM ~ RTs + (1 | stimulus) + (1 | subjects)

################# Active1 start Maximum PostM ############################

#Для одного сенсора
df <- read.csv('active1_st_93.csv')
### превращаем нужные переменные в факторы ###
df$stimulus <- factor(df$stimulus)
df$subjects <- factor(df$subjects)

#строим модель
Model <- lmer(max_beta_PostM ~ RTs + (1 + RTs|subjects) + (1 + RTs|stimulus), data=df)
summary(Model)

s <- step(Model) #автоматически ищем упрощенную модель
s
#по сенсору выбранному с помощью full LM
#s - выдает предупрежедения и упрощенную модель
#Model found:
#max_beta_PostM ~ RTs + (1 | subjects) 

############################## Active2 end Minimum PreM ################################

#Для одного сенсора
df <- read.csv('active2_end_69.csv')
### превращаем нужные переменные в факторы ###
df$stimulus <- factor(df$stimulus)
df$subjects <- factor(df$subjects)

#строим модель
Model <- lmer(min_beta_PreM ~ RTs + (1 + RTs|subjects) + (1 + RTs|stimulus), data=df)
summary(Model)

s <- step(Model) #автоматически ищем упрощенную модель
s
#по сенсору выбранному с помощью full LM
#s - выдает предупрежедения и упрощенную модель 
#Model found:
#min_beta_PreM ~ RTs + (1 | subjects) 

################################# Active2 end Maximum PostM  ############################

#Для одного сенсора
df <- read.csv('active2_end_8.csv')
### превращаем нужные переменные в факторы ###
df$stimulus <- factor(df$stimulus)
df$subjects <- factor(df$subjects)

#строим модель
Model <- lmer(max_beta_PostM ~ RTs + (1 + RTs|subjects) + (1 + RTs|stimulus), data=df)
summary(Model)

s <- step(Model) #автоматически ищем упрощенную модель
s
#по сенсору выбранному с помощью full LM
#s - выдает предупрежедения и упрощенную модель 
#Model found:
#max_beta_PostM ~ RTs + (1 | stimulus) + (1 | subjects)


########################################################################################
##################### Шаг 3. Обучаем полученные модели на всех сенсорах ################
# Анализ делаем по очереди, для этого изменяем df и модель. Также меняем рабочую директорию
#Не забываем менять название файла, куда сохраняем данные

# Построение модели для 102 сенсоров в цикле 
  # Задаем пустые списки для коэффициентов корреляции и p_value
  reg_coeff <- NULL
  p_val <- NULL
  
  # задаем список от 0 до 101
  
  num <- 0:101
  for(i in num){
    df <- read.csv(paste('active1_st_',as.character(i),'.csv',sep=''))
    ### превращаем нужные переменные в факторы ###
    df$stimulus <- factor(df$stimulus)
    df$subjects <- factor(df$subjects)
    
    # строим линейную модель со смешенными эффектами
    Model <- lmer(max_beta_PostM ~ RTs + (1 | subjects), data=df)
    
    # извлекаем необходимые значения из summary 
    Sum <- coef(summary(Model))
    x <- Sum[2,1]
    y <- Sum[2,5] 
    reg_coeff <- c(reg_coeff,x)
    p_val <- c(p_val,y)
  }
  
  #смотрим полученные значения
  #p_val
  
  #создаем dataframe из полученных в цикле списков
  dframe <- data.frame("reg_coeff" = reg_coeff, "p_val" = p_val)
  
  #записываем полученный dataframe в csv файл
  write.csv(dframe,"active1_st_maximum_beta_PostM_choose_by_full_LMEM.csv", row.names = FALSE)
  