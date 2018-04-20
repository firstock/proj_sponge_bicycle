getwd()
setwd("C:\\github\\proj_sponge_bicycle\\data_join\\totalByArea")
# data <- read.csv("광진구.csv", header = T)
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
data <- data[,c(1:15, 17, 18, 23, 24)]
str(data)
data <- data.frame(scale(data, scale = T, center = T))
head(data);str(data);dim(data)

X <- data[,2:19]
y <- data[,1]

# Tuning Random Forest
#standard Random Forest
rf1 = randomForest(X, y, ntree = 5000) 
print(rf1)
plot(rf1,log="x",main="black default, red samplesize, green tree depth")

#reduced sample size
rf2 = randomForest(X, y, sampsize = .1*length(y), ntree = 5000) 
print(rf2)
points(1:5000,rf2$mse,col="red",type="l")

#limiting tree depth
rf3 = randomForest(X, y, maxnodes = 24, ntree = 5000)
print(rf2)
points(1:5000,rf3$mse,col="darkgreen",type="l")

# Tuning Gradient Boosting
# install.packages("caret")
library(caret)
grid<-expand.grid(.n.trees=seq(100,5000,by=200),.interaction.depth=seq(1,4,by=1),.shrinkage=c(.001,.01,.1),
                  .n.minobsinnode=10)
control<-trainControl(method = "CV")
gbm.train<-train(rentcnt~.,data=data,method='gbm',trControl=control)
gbm.train
