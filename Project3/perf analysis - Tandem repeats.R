 
library(tidyverse)

setwd("C:/Docs/Drive/Uni/18F/Genome scale algorithms/Project 1")

df_Raw = read.csv("Test - SuffixTree Tandem Repeats.csv", header = FALSE)

colnames(df_Raw) = c("Function", "Time", "RunName", "n", "z")

df_Raw$RunName = factor(x = df_Raw$RunName)
df_Raw$Function = factor(x = df_Raw$Function)

runs = levels(df_Raw$RunName)
run.fib = runs[1]
run.rand = runs[2]
run.dna = runs[3]

df_dna = df_Raw[df_Raw$RunName == run.dna,]
df_fib = df_Raw[df_Raw$RunName == run.fib,]

df_test = df_fib

cleaner = function( l.Time )
{
  l.Time = c(l.Time)
  if( length( l.Time ) < 3)
  {
    return (-1)
  }
  
  # sort
  l.Time = sort(l.Time)
  # remove max val
  l.max2 = l.Time[1:(length(l.Time)-1)]
  v.max = max(l.max2)
  v.min = min(l.max2)
  #l.norm = (l.max2 - v.min) / (v.max - v.min)
  v.mean = mean(l.max2)
  l.Time = l.Time[l.Time < v.mean]
  
  mean(l.Time)
  
}
cleaner( c(1,2,2,2,3,3,8,9,11,15,16))


df_t2 = df_test %>% group_by( n ) %>% summarise( cnt = n(), Time.p = cleaner( Time ), Time.mean = my.mean( n )  )
df_t2 = df_t2[df_t2$cnt > 2,]

ggplot( ) +
  geom_point( data = df_test, aes( y = Time, x = n  ), color = "#ff0000", alpha = 0.3 ) +
  geom_point( data = df_t2, aes( y = Time.p, x = n  ), color = "#0000ff", alpha = 0.6 )


fit_n2 = lm( data = df_test, formula = Time ~ I(n**2) + I(n) )
fit_n2 = lm( data = df_test, formula = Time ~ poly(n,2) )

fit_logn = lm( data = df_test, formula = Time ~ log(n) * n )
fit_nz = lm( data = df_test, formula = Time ~ n + z )
fit_lognz = lm( data = df_test, formula = Time ~ log(n) * n + z )

fit_ex = lm( data = df_test, formula = log(Time) ~ n )

#fit_ex <- nls(Time ~ exp(a + b *n), data = df_test, start = list(a = 0, b = 0))

fit_n2
fit_logn
fit_lognz

sum(fit_n2$residuals**2)
sum(fit_logn$residuals**2)
sum(fit_lognz$residuals**2)

anova(fit_n2, fit_logn)
anova(fit_logn, fit_lognz)

df_test$fit1 = 
  fit_n2$coefficients["I(n^2)"] * df_test$n**2 + 
  fit_n2$coefficients["I(n)"] * df_test$n + 
  fit_n2$coefficients["(Intercept)"]

df_test$fit2 = 
  fit_logn$coefficients["log(n):n"] * df_test$n * log(df_test$n) + 
  fit_logn$coefficients["log(n)"] * log(df_test$n) + 
  fit_logn$coefficients["n"] * df_test$n + 
  fit_logn$coefficients["(Intercept)"]

df_test$fit3 = 
  fit_nz$coefficients["n"] * df_test$n + 
  fit_nz$coefficients["z"] * df_test$z + 
  fit_nz$coefficients["(Intercept)"]

df_test$fit4 = 
  fit_lognz$coefficients["log(n):n"] * df_test$n * log(df_test$n) + 
  fit_lognz$coefficients["log(n)"] * log(df_test$n) + 
  fit_lognz$coefficients["n"] * df_test$n + 
  fit_lognz$coefficients["z"] * df_test$z + 
  fit_lognz$coefficients["(Intercept)"]

df_test$fit5 = exp(
  fit_ex$coefficients["n"] * df_test$n + 
  fit_ex$coefficients["(Intercept)"]
)

ggplot( data = df_test[,] ) +
  geom_point( aes( y = Time, x = n  ), color = "#000000", alpha = 0.8 )


ggplot( data = df_test[,] ) +
  geom_point( aes( y = Time, x = z  ), color = "#000000", alpha = 0.8 )

ggplot( data = df_test[,] ) +
  geom_point( aes( y = Time, x = n  ), color = "#000000", alpha = 0.8 ) +
  geom_point( aes( y = fit1, x = n  ), color = "#ff0000", alpha = 0.6 ) +
  geom_point( aes( y = fit2, x = n  ), color = "#00ff00", alpha = 0.6 ) +
  #geom_point( aes( y = fit3, x = n  ), color = "#0000ff", alpha = 0.6 ) +
  geom_point( aes( y = fit4, x = n  ), color = "#0000ff", alpha = 0.6 )

ggplot( data = df_test[,] ) +
  geom_point( aes( y = Time, x = n  ), color = "#000000", alpha = 0.8 ) +
  geom_point( aes( y =  1.309e-04 * n * log(n) + -1.106e-03 * n, x = n ), color = "#ff0000", alpha = 0.6 ) 
  
fit_lognz
  

ggplot( data = df_test[,] ) +
  geom_point( aes( y = Time / fit1, x = fit1  ), color = "#ff0000", alpha = 0.6 ) +
  geom_point( aes( y = Time / fit2, x = fit2  ), color = "#00ff00", alpha = 0.6 ) +
  geom_point( aes( y = Time / fit4, x = fit4  ), color = "#0000ff", alpha = 0.6 ) +
  ylim(0,2) + xlim(0.1,1.6)







ggplot( data = df_tvpc ) +
  geom_point( aes( y = Time, x = n  ) )

ggplot( data = df_tvpv ) +
  geom_point( aes( y = Time, x = n + m  ) )


ggplot( data = df_Raw ) +
  geom_point( aes( y = Time, x = m * z ), color = "#00ff00", alpha = 0.5 ) 

ggplot( data = df_Raw ) +
  geom_point( aes( y = Time, x = m  ), color = "#00ff00", alpha = 0.5 ) +
  geom_point( aes( y = Time, x = n  ), color = "#ff0000", alpha = 0.2 ) +
  geom_point( aes( y = Time, x = n * m * 0.001  ), color = "#ff00ff", alpha = 0.2 )


#fit_tcpv = glm( data = df_tcpv, formula = Time ~ m)

fit_c = lm( data = df_Raw, formula = Time ~ 1)
fit_m = lm( data = df_Raw, formula = Time ~ m)
fit_n = lm( data = df_Raw, formula = Time ~ n)
fit_z = lm( data = df_Raw, formula = Time ~ z)
fit_nm = lm( data = df_Raw, formula = Time ~ m + n)
fit_nmz = lm( data = df_Raw, formula = Time ~ m + n + z)
fit_nm_z.n = lm( data = df_Raw, formula = Time ~ m + n + z * n)
fit_nm_z.m = lm( data = df_Raw, formula = Time ~ m + n + z * m)
fit_nm_n.m = lm( data = df_Raw, formula = Time ~ m + n + m * n)
fit_nm_z.mn = lm( data = df_Raw, formula = Time ~ m + n + z * m * n)

fit_nm_ln = lm( data = df_Raw, formula = Time ~ m + n + log(n))
fit_nm_lm = lm( data = df_Raw, formula = Time ~ m + n + log(m))

fit_impl = lm( data = df_Raw, formula = Time ~ m + n + I(m^2) )


anova(fit_c, fit_m)
anova(fit_c, fit_n)
anova(fit_n, fit_nm)
anova(fit_nm, fit_nmz)
anova(fit_nm, fit_nm_ln)
anova(fit_nm, fit_nm_lm)
anova(fit_nm, fit_impl)

anova(fit_nm, fit_nm_z.n)
anova(fit_nm, fit_nm_z.m)
anova(fit_nm, fit_nm_z.mn)
anova(fit_nm, fit_nm_n.m) # 0.01749 * !!!

fit_nm
fit_nm_n.m
fit_nm_z.mn
fit_nm_lm

fit_impl

ggplot( data = df_Raw ) +
  geom_point( aes( y = Time, x = m * 3.741e-06 + 4.399e-07 * n ), color = "#000000", alpha = 0.9 ) +
  geom_point( aes( y = Time, x = m * 3.544e-06 + 4.260e-07 * n + n * m * 1.522e-11 ), color = "#ff0000", alpha = 0.3 ) +
  geom_point( aes( y = Time, x = m * 3.544e-06 + 4.260e-07 * n + log(m) * -7.368e-05 ), color = "#00ff00", alpha = 0.3 ) +
  geom_point( aes( y = Time, x = m * 3.755e-06 + 4.371e-07 * n + 2.305e-10 * m**2 ), color = "#0000ff", alpha = 0.3 )
  
  
ggplot( data = df_Raw[10:2000,] ) +
  geom_point( aes( y = Time, x = m * 3.834e-06, size = z ), color = "#000000", alpha = 0.3 )
  #geom_point( aes( y = Time, x = m * 3.544e-06 + 4.260e-07 * n + n * m * 1.522e-11 ), color = "#ff0000", alpha = 0.3 ) +
  #geom_point( aes( y = Time, x = m * 3.544e-06 + 4.260e-07 * n + log(m) * -7.368e-05 ), color = "#00ff00", alpha = 0.3 ) +
  #geom_point( aes( y = Time, x = m * 3.755e-06 + 4.371e-07 * n + 2.305e-10 * m**2 ), color = "#0000ff", alpha = 0.3 )


fit_nm = lm( data = df_Raw[10:2000,], formula = Time ~ m)
fit_nmz = lm( data = df_Raw[10:2000,], formula = Time ~ m + z * m)
fit_nm
fit_nmz
anova(fit_nmz, fit_nmz)






