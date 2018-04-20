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
data <- read.csv("중구.csv", header = T)

dim(data);head(data)
data <- data[, 3:26]
data <- data[,c(1:15, 17, 18, 23, 24)]
str(data)
data <- data.frame(scale(data, scale = T, center = T))
head(data);str(data);dim(data)

# modeling
set.seed(1)
################################################################
# # Lasso for 10-fold cross-validation
# install.packages("glmnet")
library(glmnet)
x <- data[,2:19]
y <- data[,1]
fit.lasso <- glmnet(as.matrix(x), y, family = "gaussian", alpha = 1)
cv.lasso <- cv.glmnet(as.matrix(x), y, nfolds = 10, family = "gaussian", alpha = 1, lambda = fit.lasso$lambda)
plot(cv.lasso)
abline(v=log(cv.lasso$lambda.min), col="red")
abline(v=log(cv.lasso$lambda.1se), col="blue")
legend("topleft", legend = c("log(lambda.min)", "log(lambda.1se)"), col=c("red", "blue"), lwd = 2)

fit.lasso.param <- cv.lasso$lambda.min
# fit.lasso.param <- cv.lasso$lambda.1se
fit.lasso.tune <- glmnet(as.matrix(x), y, family = "gaussian", alpha = 1, lambda = fit.lasso.param)
coef(fit.lasso.tune)

lasso.pred <- predict(fit.lasso.tune, newx = as.matrix(x), type = "response")
lasso.error <- lasso.pred - y
sqrt(mean(lasso.error^2)) # RMSE of Lasso

################################################################################
# Ridge for 10-fold cross-validation
fit.ridge <- glmnet(as.matrix(x), y, family = "gaussian", alpha = 0)
cv.ridge <- cv.glmnet(as.matrix(x), y, nfolds = 10, family = "gaussian", alpha = 0, lambda = fit.ridge$lambda)
plot(cv.ridge)
abline(v=log(cv.ridge$lambda.min), col="red")
abline(v=log(cv.ridge$lambda.1se), col="blue")
legend("bottomright", legend = c("log(lambda.min)", "log(lambda.1se)"), col=c("red", "blue"), lwd = 2)

fit.ridge.param <- cv.ridge$lambda.min
# fit.ridge.param <- cv.ridge$lambda.1se
fit.ridge.tune <- glmnet(as.matrix(x), y, family = "gaussian", alpha = 0, lambda = fit.ridge.param)
coef(fit.ridge.tune)

ridge.pred <- predict(fit.ridge.tune, newx = as.matrix(x), type = "response")
ridge.error <- ridge.pred - y
sqrt(mean(ridge.error^2)) # RMSE of Ridge

####################################################################################
# Elastic Net for 10-fold cross-validation
fit.elastic <- glmnet(as.matrix(x), y, family = "gaussian", alpha = .5)
cv.elastic <- cv.glmnet(as.matrix(x), y, nfolds = 10, family = "gaussian", alpha = .5, lambda = fit.elastic$lambda)
plot(cv.elastic)
abline(v=log(cv.elastic$lambda.min), col="red")
abline(v=log(cv.elastic$lambda.1se), col="blue")
legend("bottomright", legend = c("log(lambda.min)", "log(lambda.1se)"), col=c("red", "blue"), lwd = 2)

fit.elastic.param <- cv.elastic$lambda.min
# fit.elastic.param <- cv.elastic$lambda.1se
fit.elastic.tune <- glmnet(as.matrix(x), y, family = "gaussian", alpha = .5, lambda = fit.elastic.param)
coef(fit.elastic.tune)

elastic.pred <- predict(fit.elastic.tune, newx = as.matrix(x), type = "response")
elastic.error <- elastic.pred - y
sqrt(mean(elastic.error^2)) # RMSE of Elastic Net

##########################################################################
# Random forest
# install.packages("randomForest")
library(randomForest)
fit.rf <- randomForest(rentcnt ~., data = data, ntree = 5000)
rf.pred <- fit.rf$predicted
rf.error <- rf.pred - data[["rentcnt"]]
sqrt(mean(rf.error^2)) # RMSE of random forest

importance(fit.rf)
varImpPlot(fit.rf)

###########################################################################
# SVR for 10-fold cross-validation
# install.packages("e1071")
library(e1071)
fit.svr <- svm(rentcnt ~ ., kernel = "radial", cross = 10, data = data)
summary(fit.svr)
# names(fit.svr)
mean(sqrt(fit.svr$MSE)) # RMSE of SVR

###################################################
# Decision tree for 10-fold cross validation
# install.packages("tree")
library(tree)
cv.folds <- function (n, folds = 10) {
  split(sample(1:n), rep(1:folds, length = n))
}

(K <- 10)
# (K <- nrow(dat))
(all.folds <- cv.folds(nrow(data), K))
str(all.folds)

cv.RMSE <- NULL
for(j in 1:K){
  test  <- all.folds[[j]]
  fit.tree <- tree(rentcnt ~ ., data=data[-test,])
  tree.pred  <- predict(fit.tree, data[test,])
  cv.RMSE[j] <- sqrt(sum((data[test,]$rentcnt - tree.pred)^2)/length(tree.pred))
}
list(cv.RMSE, mean(cv.RMSE)) # RMSE of decision tree

par(mfrow=c(1,2))
cv.fit.tree <- cv.tree(fit.tree, K = 10)
names(cv.fit.tree)
plot(cv.fit.tree$size, cv.fit.tree$dev, type = "b", main = "Optimal Tree Size")
prune.fit.tree <- prune.tree(fit.tree, best = 8)
prune.fit.tree
plot(prune.fit.tree)
text(prune.fit.tree)

#########################################################
##Gradient Boosting for 10-fold cross validation##
# install.packages("gbm")
library(gbm)
cv.folds <- function (n, folds = 10) {
  split(sample(1:n), rep(1:folds, length = n))
}

(K <- 10)
# (K <- nrow(dat))
(all.folds <- cv.folds(nrow(data), K))
str(all.folds)

cv.RMSE <- NULL
for(j in 1:K){
  test  <- all.folds[[j]]
  model <- gbm(rentcnt ~ ., data=data[-test,], distribution = "gaussian", n.trees = 150, shrinkage = 0.1, interaction.depth = 3, n.minobsinnode = 10)
  pred  <- predict.gbm(model, data[test,], n.trees = 150)
  cv.RMSE[j] <- sqrt(sum((data[test,]$rentcnt - pred)^2)/length(pred))
}
list(cv.RMSE, mean(cv.RMSE))

summary(model)

#########################################################
##knn for 10-fold cross validation##
# install.packages("FNN")
library(FNN)
cv.folds <- function (n, folds = 10) {
  split(sample(1:n), rep(1:folds, length = n))
}

(K <- 10)
# (K <- nrow(dat))
(all.folds <- cv.folds(nrow(data), K))
str(all.folds)

cv.RMSE <- NULL
for(j in 1:K){
  test  <- all.folds[[j]]
  model <- knn.reg(train = data[-test,], test = data[test,], y = data$rentcnt, k = 3, algorithm = "kd_tree")
  pred  <- model$pred
  cv.RMSE[j] <- sqrt(sum((data[test,]$rentcnt - pred)^2)/length(pred))
}
list(cv.RMSE, mean(cv.RMSE))

########## END ######################
##############################################################
# neural network for 10-fold cross validation
# install.packages("neuralnet")
# library(neuralnet)
# error <- vector()
# for (i in 1:10) {
#   fit.neuralnet <- neuralnet(total_rental ~ m.temp + m.atmos + m.see_level.pre + m.water_vap + 
#                                m.dew_point + m.rel_hum + s.a_precipitation + m.windspeed + 
#                                m.a_cloud + m.mla_cloud + p.sunshine + s.a_snow + m.min_temp + 
#                                m.gs_temp + total_census + n_dioxide + ozone + c_monoxide + 
#                                s_dioxide + fp_matter, data = data, hidden = i)
#   real = fit.neuralnet$response
#   net = fit.neuralnet$net.result
#   net = unlist(net)
#   res = data
#   err = sum((net - res)^2)/2
#   error = c(error, err)
# }
# 
# plot(x = 1:10, y = error)
# # str(fit.neuralnet)
# 
# 
# cv.folds <- function (n, folds = 10) {
#   split(sample(1:n), rep(1:folds, length = n))
# }
# 
# (K <- 10)
# # (K <- nrow(dat))
# (all.folds <- cv.folds(nrow(data), K))
# str(all.folds)
# 
# cv.RMSE <- NULL
# for(j in 1:K){
#   test  <- all.folds[[j]]
#   model <- neuralnet(total_rental ~ m.temp + m.atmos + m.see_level.pre + m.water_vap + 
#                        m.dew_point + m.rel_hum + s.a_precipitation + m.windspeed + 
#                        m.a_cloud + m.mla_cloud + p.sunshine + s.a_snow + m.min_temp + 
#                        m.gs_temp + total_census + n_dioxide + ozone + c_monoxide + 
#                        s_dioxide + fp_matter, data=data[-test,], hidden = 1)
#   pred  <- prediction(model, data[test,])
#   cv.RMSE[j] <- sqrt(sum((data[test,]$total_rental - pred)^2)/length(pred))
# }
# list(cv.RMSE, mean(cv.RMSE))
# 
# names(fit.neuralnet)
# 
# fit.neuralnet$err.fct
# 
# plot(fit.neuralnet)

###########################################################
# # Multiple Linear Regression for 10-fold cross validation
# cv.folds <- function (n, folds = 10) {
#   split(sample(1:n), rep(1:folds, length = n))
# }
# 
# (K <- 10)
# # (K <- nrow(dat))
# (all.folds <- cv.folds(nrow(data), K))
# str(all.folds)
# 
# cv.RMSE <- NULL
# for(j in 1:K){
#   test  <- all.folds[[j]]
#   model <- lm(rentcnt ~ ., data=data[-test,])
#   pred  <- predict(model, data[test,])
#   cv.RMSE[j] <- sqrt(sum((data[test,]$rentcnt - pred)^2)/length(pred))
# }
# list(cv.RMSE, mean(cv.RMSE)) # RMSE of Multiple Linear Regression

