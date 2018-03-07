 

library(tidyverse)

setwd("C:/Docs/Drive/Uni/18F/Genome scale algorithms/Project 1")

# Load data

df_build.naive = read.csv( "Test - SuffixTree Build - Naive.csv" )
colnames(df_build.naive) = c("Function", "Time", "Test", "text.len", "pattern.len", "occurrences", "?")
df_search = read.csv( "Test - SuffixTree Search.csv" )
colnames(df_search) = c("Function", "Time", "Test", "text.len", "pattern.len", "occurrences", "?")

df_build.naive_aaa = df_build.naive[1:2999,]
df_build.naive_aab = df_build.naive[3000:4199,]

# Test - the test type:
# aaa-Tc-Px : all a's, text length is constant, pattern length is variable 
# aaa-Tx-Pc : all a's, text length is variable, pattern length is constant 
# aaa-Tx-Px : all a's, text length is variable, pattern length is variable 
# aab-Tx-Px : text is aaa..b, pattern is all a's, ...
# ...

unique(df_search$Test)


# Simple plots
ggplot( data = df_build.naive ) +
  geom_point( aes( x = text.len, y = Time, color = Test) )

ggplot( data = df_search ) +
  geom_point( aes( x = text.len, y = Time, color = Test) )

# Fit build, n^2
fit_build.naive.n2 = lm( data = df_build.naive, formula = Time ~ poly(text.len, 2) )

c0 = fit_build.naive.n2$coefficients["(Intercept)"]
cn1 = fit_build.naive.n2$coefficients["poly(text.len, 2)1"]
cn2 = fit_build.naive.n2$coefficients["poly(text.len, 2)2"]

ggplot( data = df_build.naive ) +
  geom_point( aes( x = c0 + cn1 * text.len + cn2 * text.len**2, y = Time / ( c0 + cn1 * text.len + cn2 * text.len**2 ) ) )

# Fit search
fit_search.linear = lm( data = df_search, formula = Time ~ pattern.len )

cm0 = fit_search.linear$coefficients["(Intercept)"]
cm1 = fit_search.linear$coefficients["pattern.len"]

ggplot( data = df_search ) +
  geom_point( aes( x = cm0 + cm1 * pattern.len , y = Time / ( cm0 + cm1 * pattern.len ) ) )


