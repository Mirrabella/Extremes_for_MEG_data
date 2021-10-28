# Выбор значимых для Актива 1 и Актива 2 конец сенсоров и построения scatterplots для них
# Список сенсоров Probing MEG0132 - 2, MEG0222 - 5, MEG1522 - 55, 
# Targeted MEG1842 - 69, MEG0312 - 8, MEG0332 - 10, 




########################## PreMovements #########################

df1 <- read.csv('/home/vera/MNE/MEM_regression/MEM_old_right_baseline/table_for_mem_active1_st/active1_st_2.csv')
sust
df2 <- read.csv('/home/vera/MNE/MEM_regression/MEM_old_right_baseline/table_for_mem_active2_end/active2_end_69.csv')

M_reg1 <- lm(beta_power_PreM ~ RTs, data=df1)
df1$reg_pred_PreM <- predict(M_reg1)
M_reg2 <- lm(beta_power_PreM ~ RTs, data=df2)
df2$reg_pred_PreM <- predict(M_reg2)

fig1 <- ggplot(data = df1, aes(x = RTs, y = beta_power_PreM)) + 
  geom_point() + 
  geom_line(data = df1, aes(x = RTs, y = reg_pred_PreM), col = 'blue', size = 1)

#ссылка как работать с ggplot https://matrunich.com/blog/2014/06/17/ggplot2_axes_legend_titles/
fig1 + ggtitle("Response time ~ Beta power, PreM interval, Probing MEG0132") +
  xlab("RTs (Response time), s") + ylab("Beta power")

# сохраняем рисунок на диск
dev.print(pdf, '/home/vera/MNE/MEM_regression/MEM_old_right_baseline/Probing_PreM_MEG0132.pdf')

fig2 <- ggplot(data = df2, aes(x = RTs, y = beta_power_PreM)) + 
  geom_point() + 
  geom_line(data = df2, aes(x = RTs, y = reg_pred_PreM), col = 'blue', size = 1)

#ссылка как работать с ggplot https://matrunich.com/blog/2014/06/17/ggplot2_axes_legend_titles/
fig2 + ggtitle("Response time ~ Beta power, PreM interval, Targeted MEG1642") +
  xlab("RTs (Response time), s") + ylab("Beta power")

# сохраняем рисунок на диск
dev.print(pdf, '/home/vera/MNE/MEM_regression/MEM_old_right_baseline/Targeted_PreM_MEG1842.pdf')

################## Movement ######################

  df1 <- read.csv('/home/vera/MNE/MEM_regression/MEM_old_right_baseline/table_for_mem_active1_st/active1_st_77.csv')
  
  df2 <- read.csv('/home/vera/MNE/MEM_regression/MEM_old_right_baseline/table_for_mem_active2_end/active2_end_100.csv')
  
  M_reg1 <- lm(beta_power_M ~ RTs, data=df1)
  df1$reg_pred_M <- predict(M_reg1)
  M_reg2 <- lm(beta_power_M ~ RTs, data=df2)
  df2$reg_pred_M <- predict(M_reg2)
  
  fig1 <- ggplot(data = df1, aes(x = RTs, y = beta_power_M)) + 
    geom_point() + 
    geom_line(data = df1, aes(x = RTs, y = reg_pred_M), col = 'blue', size = 1)
  
  #ссылка как работать с ggplot https://matrunich.com/blog/2014/06/17/ggplot2_axes_legend_titles/
  fig1 + ggtitle("Response time ~ Beta power, M interval, Probing MEG2042") +
    xlab("RTs (Response time), s") + ylab("Beta power")
  
  # сохраняем рисунок на диск
  dev.print(pdf, '/home/vera/MNE/MEM_regression/MEM_old_right_baseline/Probing_M_MEG2042.pdf')
  
  fig2 <- ggplot(data = df2, aes(x = RTs, y = beta_power_M)) + 
    geom_point() + 
    geom_line(data = df2, aes(x = RTs, y = reg_pred_M), col = 'blue', size = 1)
  
  #ссылка как работать с ggplot https://matrunich.com/blog/2014/06/17/ggplot2_axes_legend_titles/
  fig2 + ggtitle("Response time ~ Beta power, M interval, Targeted MEG2632") +
    xlab("RTs (Response time), s") + ylab("Beta power")
  
  # сохраняем рисунок на диск
  dev.print(pdf, '/home/vera/MNE/MEM_regression/MEM_old_right_baseline/Targeted_M_MEG2632.pdf')

################## Post Movement ######################

df1 <- read.csv('/home/vera/MNE/MEM_regression/MEM_old_right_baseline/table_for_mem_active1_st/active1_st_55.csv')
sust
df2 <- read.csv('/home/vera/MNE/MEM_regression/MEM_old_right_baseline/table_for_mem_active2_end/active2_end_10.csv')

M_reg1 <- lm(beta_power_PostM ~ RTs, data=df1)
df1$reg_pred_PostM <- predict(M_reg1)
M_reg2 <- lm(beta_power_PostM ~ RTs, data=df2)
df2$reg_pred_PostM <- predict(M_reg2)

fig1 <- ggplot(data = df1, aes(x = RTs, y = beta_power_PostM)) + 
  geom_point() + 
  geom_line(data = df1, aes(x = RTs, y = reg_pred_PostM), col = 'blue', size = 1)

#ссылка как работать с ggplot https://matrunich.com/blog/2014/06/17/ggplot2_axes_legend_titles/
fig1 + ggtitle("Response time ~ Beta power, PostM interval, Probing MEG1522") +
  xlab("RTs (Response time), s") + ylab("Beta power")

# сохраняем рисунок на диск
dev.print(pdf, '/home/vera/MNE/MEM_regression/MEM_old_right_baseline/Probing_PostM_MEG1522.pdf')

fig2 <- ggplot(data = df2, aes(x = RTs, y = beta_power_PostM)) + 
  geom_point() + 
  geom_line(data = df2, aes(x = RTs, y = reg_pred_PostM), col = 'blue', size = 1)

#ссылка как работать с ggplot https://matrunich.com/blog/2014/06/17/ggplot2_axes_legend_titles/
fig2 + ggtitle("Response time ~ Beta power, PostM interval, Targeted MEG0332") +
  xlab("RTs (Response time), s") + ylab("Beta power")

# сохраняем рисунок на диск
dev.print(pdf, '/home/vera/MNE/MEM_regression/MEM_old_right_baseline/Targeted_PostM_MEG0332.pdf')

