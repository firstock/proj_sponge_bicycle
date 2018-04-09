# R 트위터 분석 배운 코드 그대로!!
# twitter
# install.packages("twitteR")
# install.packages(c("ROAuth", "plyr", "stringr", "RJSONIO", "RCUrl", "ggplot2"))
library(twitteR)
library(ROAuth)
library(plyr)
library(stringr)
library(RJSONIO)
library(RCurl)
library(ggplot2)

consumerKey <- "lntNcVVwlkrucA1lNh7OlKLEe"
consumerSecret <- "rqzU6Rpbsn0l0Z3xAf9E8wu6wy0CG2zGQR2lpwWP3vZxFbpglN"
requestURL <- "https://api.twitter.com/oauth/request_token"
authURL <- "https://api.twitter.com/oauth/authorize"
accessURL <- "https://api.twitter.com/oauth/access_token"

twitCred <- OAuthFactory$new(
  consumerKey = consumerKey,
  consumerSecret = consumerSecret,
  requestURL = requestURL,
  accessURL = accessURL,
  authURL = authURL)

library(devtools)
install_github("twitteR", username = "geoffjentry")
library(twitteR)

setup_twitter_oauth("lntNcVVwlkrucA1lNh7OlKLEe",
                    "rqzU6Rpbsn0l0Z3xAf9E8wu6wy0CG2zGQR2lpwWP3vZxFbpglN",
                    access_token = "954249281702998016-OWZf5z6QywhqtogveBWPwFA0qWAjXqv",
                    access_secret = "NdKA7hVvFvsrgiTPKphGuS1wB6U3IEQUJWCTfRVJIM4TS")

# install_github("twitteR", username = "geoffjentry", force = T)

n <- 2000
keyword <- '공공자전거'
keyword <- enc2utf8(keyword)
tweets2 <- searchTwitter(keyword, n)
Rangers_df <- do.call("rbind", lapply(tweets2, as.data.frame))
write.csv(Rangers_df, "twitter.csv")

tweet <- read.csv("twitter.csv")
#특수문자 삭제 @ 같은
# ?str_replace_all
# install.packages("stringr")
library(stringr)
tweet$text<-str_replace_all(tweet$text,"\\W"," ")
head(tweet$text)
# install.packages("KoNLP") #형태소 분석 패키지
# install.packages("wordcloud") #워드클라우드 패키지
# install.packages("RColorBrewer") #색상패키지
# Sys.setenv(JAVA_HOME='c:/Program Files/Java/jer1.8.0_161')
library(KoNLP)
library(wordcloud)
library(RColorBrewer) 
useSejongDic()  #세종사전 활용하기
#명사추출
myword<-sapply(tweet$text, extractNoun, USE.NAMES = T)
myword
#list->unlist
gogo<-unlist(myword)
head(gogo)
#필요없는 단어 삭제하기
gogo<-gsub("\\d+","",gogo) #모든 숫자 없애기
gogo<-gsub("RT","",gogo)
gogo<-gsub("SSUL_","",gogo)
gogo<-gsub("최애에","",gogo)
gogo<-gsub(" ","",gogo)
gogo<-Filter(function(x){nchar(x)>1},gogo)
gogo<-sapply(gogo, function(x){Filter(function(y){nchar(y)<=8&&nchar(y)>1&&is.hangul(y)},x)})
#한글, 8자 이하만 필터링
#워드클라우드를 만들기 위해 단어만 수집된 텍스트 파일을 만드는 작업을 해준다
write(unlist(gogo),"screen_tweet.txt") #텍스트 파일로 저장
tweet_cloud<-read.table("screen_tweet.txt") #다시불러오기
head(tweet_cloud)
#table(분할표) 만들기
wordcount<-table(tweet_cloud) #단어카운트
wordcount<-gsub("민호","",wordcount) #필요없는단어 다시 삭제
wordcount<-gsub("염력","",wordcount) #필요없는단어 다시 삭제
#다시 파일 저장
write(unlist(gogo),"screen_tweet.txt") # 이 파일 중요 !! 메모장에서 목록 확인 필수!!
tweet_cloud<-read.table("screen_tweet.txt") #다시 불러오기
wordcount<-table(tweet_cloud) #다시 table만들기
#워드클라우드생성
palete<-brewer.pal(10,"Set1") #색상 설정
wordcloud(names(wordcount),freq = wordcount, min.freq = 5, random.order=F, random.color=F, colors=palete)  

# create word-document table
df2 <- read.csv("bycle.csv", stringsAsFactors = F)
str(df2)
head(df2)
colnames(df2)
rules <- sapply(df2$text, strsplit, " ", USE.NAMES = F)
# rules[[1]]

# install.packages("tm")
library(tm)
reV <- unlist(rules)
revec <- VectorSource(rules)
revecco <- Corpus(revec)
rmyTdm <- TermDocumentMatrix(revecco, control = list(wordLengths = c(2, Inf)))
str(rmyTdm)

typeof(rmyTdm$dimnames$Terms)

findAssocs(rmyTdm, '자전거', 0.1)
inspect(rmyTdm[1:20, 1:20])

