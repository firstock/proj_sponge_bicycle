# 동아닷컴 크롤링!!
getwd()
setwd("C:/Rproject")
# install.packages("rvest")
# install.packages("dplyr")
library(rvest)
library(dplyr)
# 원하는 url 주소 basic_url 부분 삽입!!
basic_url <- 'http://news.donga.com/search?query=공공자전거&more=1&range=3&p='
urls <- NULL
for(x in 0:5){
  urls[x+1] <- paste0(basic_url, as.character(x*15+1))
}
links <- NULL
for(url in urls){
  html <- read_html(url)
  links <- c(links, html %>% html_nodes('.searchCont') %>% html_nodes('a') %>% html_attr('href') %>% unique())
}
links <- links[-grep("pdf", links)]

txts <- NULL
for(link in links){
  html <- read_html(link)
  txts <- c(txts, html %>% html_nodes('.article_txt') %>% html_text())
}

write.csv(txts, "text.csv")

tweet <- read.csv("text.csv")
#특수문자 삭제 @ 같은
# ?str_replace_all
# install.packages("stringr")
library(stringr)
tweet$x<-str_replace_all(tweet$x,"\\W"," ")
head(tweet$x)
# install.packages("KoNLP") #형태소 분석 패키지
# install.packages("wordcloud") #워드클라우드 패키지
# install.packages("RColorBrewer") #색상패키지
# Sys.setenv(JAVA_HOME='c:/Program Files/Java/jer1.8.0_161')
library(KoNLP)
library(wordcloud)
library(RColorBrewer) 
useSejongDic()  #세종사전 활용하기
#명사추출
myword<-sapply(tweet$x, extractNoun, USE.NAMES = T)
#myword
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
write(unlist(gogo),"screen_tweet.txt") # 이 파일 중요!! 메모장에서 목록 확인 필수 !!

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

# 메모장에서 불러온 두 파일 목록을 합쳐서 final.txt로 저장!!
# http://www.tagxedo.com/에서 작업하면서 마무리 !!