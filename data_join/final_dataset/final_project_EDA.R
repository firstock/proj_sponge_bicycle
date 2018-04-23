getwd()
setwd("C:\\github\\proj_sponge_bicycle\\data_join\\totalByArea")
data <- read.csv("광진구.csv", header = T)
# data <- read.csv("동대문구.csv", header = T)
# data <- read.csv("마포구.csv", header = T)
# data <- read.csv("서대문구.csv", header = T)
# data <- read.csv("성동구.csv", header = T)
# data <- read.csv("양천구.csv", header = T)
# data <- read.csv("영등포구.csv", header = T)
# data <- read.csv("용산구.csv", header = T)
# data <- read.csv("은평구.csv", header = T)
# data <- read.csv("종로구.csv", header = T)
# data <- read.csv("중구.csv", header = T)

dim(data);head(data)
data <- data[, 3:26]
data <- data[,c(1:15, 17, 18, 22, 23)]
str(data)
data <- data.frame(scale(data, scale = T, center = T))
head(data);str(data);dim(data)


library(caret)
# install.packages(c("corrplot", "Hmisc"))
library(corrplot)
library(Hmisc)

cor <- cor(data)
p.val <- rcorr(as.matrix(cor), type = "pearson")
p.val
# corrplot(cor, method = "pie")
# corrplot(cor, method = "number")
write.csv(p.val$r, "corr.csv")
write.csv(p.val$P, "pval.csv")

plot(data$rentcnt)
panel.cor <- function(x, y, digits = 2, prefix = "", cex.cor, ...) 
{ 
  usr <- par("usr"); on.exit(par(usr)) 
  par(usr = c(0, 1, 0, 1)) 
  r <- abs(cor(x, y)) 
  txt <- format(c(r, 0.123456789), digits = digits)[1] 
  txt <- paste0(prefix, txt) 
  if(missing(cex.cor)) cex.cor <- 0.8/strwidth(txt) 
  text(0.5, 0.5, txt, cex = cex.cor * r) 
} 
pairs(data, lower.panel = panel.smooth, upper.panel = panel.cor)
pairs(data, panel = panel.smooth)

