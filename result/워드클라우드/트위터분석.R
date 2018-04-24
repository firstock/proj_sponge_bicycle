setwd("E:/github/proj_sponge_bicycle/data")
tweet <- read.csv("cpNaverNewsContent.csv")
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
myword<-sapply(tweet, extractNoun, USE.NAMES = T)
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