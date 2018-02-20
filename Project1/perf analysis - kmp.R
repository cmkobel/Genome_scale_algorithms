
library(tidyverse)

setwd("C:/Docs/Drive/Uni/18F/Genome scale algorithms/Project 1")

df_Raw = read.csv("Test ExactSubstring_KMP.csv", header = FALSE)

colnames(df_Raw) = c("Function", "Time", "n", "m", "z", "RunName")

df_Raw$RunName = factor(x = df_Raw$RunName)
df_Raw$Function = factor(x = df_Raw$Function)


fit_nm = lm( data = df_Raw, formula = Time ~ m + n)
fit_nm$coefficients[1]
fit_nm$coefficients[2]
fit_nm$coefficients[3]

# Plot with Time / Full regression
ggplot( data = df_Raw ) +
  geom_line( 
    aes( 
      y = Time / ( m * fit_nm$coefficients[2] + fit_nm$coefficients[3] * n + fit_nm$coefficients[1] ), 
      x = m * fit_nm$coefficients[2] + fit_nm$coefficients[3] * n + fit_nm$coefficients[1] 
    ), 
    color = "#000000", alpha = 0.9 
  ) +
  xlim(0.0001,0.01) + ylim(0.5,6)
# Problematic around x ~ 0. Intercept is negative, this is impossible.

# Plot with Time / Regression without intercept
ggplot( data = df_Raw ) +
  geom_line( 
    aes( 
      y = Time / ( m * fit_nm$coefficients[2] + fit_nm$coefficients[3] * n  ), 
      x = m * fit_nm$coefficients[2] + fit_nm$coefficients[3] * n
    ), 
    color = "#000000", alpha = 0.9 
  ) +
  xlim(0.0001,0.01) + ylim(0.8,5)

# Flat line + random spikes? (cpu doing something diff could be enough to explain it)


