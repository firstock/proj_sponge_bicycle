# coding: utf-8
# coding: utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os.path
from os import rename, listdir, mkdir

import time

import csv
import pandas as pd
from pandas import DataFrame, Series
import numpy as np
import re


def startWeb(numPage=1):
    """
    네이버 뉴스
    검색어: 공공자전거
    옵션유지: 켜짐. mynews=1
    @return driver
    """
    driver= webdriver.Chrome('lib/chromedriver.exe')
    paging= str(1+10*(numPage-1))
    # caution: "\ is before &"
    url= "https://search.naver.com/search.naver?&where=news    &query=%EA%B3%B5%EA%B3%B5%EC%9E%90%EC%A0%84%EA%B1%B0&sm=tab_pge    &sort=0&photo=0&field=0&reporter_article=&pd=0&ds=&de=&docid=    &nso=so:r,p:all,a:all&mynews=1&start="+paging+"&refresh_start=0"
    driver.get(url)
    
    try:
        element= WebDriverWait(driver, 10).until(
            # is comming content?
            EC.presence_of_element_located((By.XPATH, '//li'))
        )
    except Exception as e:
        print('error',e)
    return driver
def searchOptPress():
    """
    일간지, 뉴시스, 연합뉴스, 한국경제TV, JTBC, 시사IN
    """
    #검색옵션
    try:
        element= WebDriverWait(driver, 10).until(
            # is comming content?
            EC.presence_of_element_located((By.XPATH, '//a[@id="_search_option_btn"]'))
        )
    except Exception as e:
        print('error',e)
    element.click()

    #언론사
    xpath1= '//li[@id="news_popup"]'
    element= driver.find_element_by_xpath(xpath1)
    element.click()

    # #전체선택 해제. '18.4.24 부로 전체선택옵션이 없어졌다 ㄷㄷ
    # xpath2= '//input[@id="select_all_order"]'
    # element= driver.find_element_by_xpath(xpath2)
    # element.click()

    #일간지 선택
    xpath3= '//input[@id="ca_p1"]'
    element= driver.find_element_by_xpath(xpath3)
    element.click()
    
    somePress= ["뉴시스", "연합뉴스", "한국경제TV", "JTBC", "시사IN"]
    for press in somePress:
        xpath= '//label[@title="'+press+'"]'
        element= driver.find_element_by_xpath(xpath)
        element.click()
        
    # 확인
    xpathChk= '//button[@class="impact _submit_btn"]'
    element= driver.find_element_by_xpath(xpathChk)
    element.click()
    
    try:
        element= WebDriverWait(driver, 10).until(
            # is comming content?
            EC.presence_of_element_located((By.XPATH, '//li'))
        )
    except Exception as e:
        print('error',e)
def movePage(numPage):
    paging= str(1+10*(numPage-1))
    url= "https://search.naver.com/search.naver?&where=news    &query=%EA%B3%B5%EA%B3%B5%EC%9E%90%EC%A0%84%EA%B1%B0&sm=tab_pge    &sort=0&photo=0&field=0&reporter_article=&pd=0&ds=&de=&docid=    &nso=so:r,p:all,a:all&mynews=1&start="+paging+"&refresh_start=0"
    driver.get(url)
    
    try:
        element= WebDriverWait(driver, 10).until(
            # is comming content?
            EC.presence_of_element_located((By.XPATH, '//div[@class="thumb"]'))
        )
    except Exception as e:
        print('error',e)
def saveLink(listLink):
    #caution: not '_sp_each_title' but ' _sp_each_title'
    #amazing: there are no duplicated. why ??
    
    xpathLink1= '//a[@class=" _sp_each_title"]'
    elements= driver.find_elements_by_xpath(xpathLink1)
    for element in elements:
        listLink.append(element.get_attribute("href"))
        
    xpathLink2= '//a[@class="_sp_each_url _sp_each_title"]'
    elements= driver.find_elements_by_xpath(xpathLink2)
    for element in elements:
        listLink.append(element.get_attribute("href"))
        
    return listLink
def movePageLink(link):
    driver.get(link)
    try:
        element= WebDriverWait(driver, 10).until(
            # is coming a content?
            EC.presence_of_element_located((By.XPATH, '//div'))
        )
    except Exception as e:
        print('error',e)
def mkDictNewsXpath():
    """
    link scraping 결과에 unique() 하고, 의뭉스런 사이트를 직접 들어가서
    해당 언론사가 필터링한 언론사 맞는지 확인한 결과
    
    xpath가 틀렸다면 여기서 정정!
    """
    link= ['news.khan.co', 'www.khan.co', 'h2.khan.co', 'news.kmib.co', 'www.naeil.com', 'news.donga.com', 'www.donga.com', 'realestate.donga.com', 'bizn.donga.com', 'travel.donga.com', 'studio.donga.com', 'yachtpia.donga.com', 'it.donga.com', 'www.m-i.kr', 'www.munhwa.com', 'www.seoul.co', 'ntn.seoul.co', 'stv.seoul.co', 'www.segye.com', 'local.segye.com', 'www.segyefn.com', 'economysegye.segye.com', 'fn.segye.com', 'www.asiatoday.co', 'news.chosun.com', 'biz.chosun.com', 'car.chosun.com', 'life.chosun.com', 'businessnews.chosun.com', 'news.joins.com', 'realestate.joins.com', 'www.hani.co', 'babytree.hani.co', '2korea.hani.co', 'www.hankookilbo.com', 'www.newsis.com', 'sports.news.naver', 'news.naver.com', 'app.yonhapnews.co', 'www.wowtv.co', 'www.wownet.co', 'news.wowtv.co', 'sports.wowtv.co', 'wowstar.wowtv.co', 'news.jtbc.co', 'www.sisain.co', 'www.sisainlive.com']
    dupCnt= [3,1,1,8,1,1,3,5,1,5,2,3,1,2,2,5,1,2]
    xpaths= ['//div[@id="articleBody"]', '//div[@id="articleBody"]', '//div[@class="articleArea"]', '//div[@id="ct"]', '//div[@class="content"]', '//div[@id="NewsAdContent"]', '//div[@id="article_content"]', '//div[@id="article_txt"]', '//div[@id="font"]', '//div[@id="news_body_id"]/div[@class="par"]', '//div[@id="article_body"]', '//div[@class="article-text-font-size"]', '//article[@id="article-body"]','//div[@itemprop="articleBody"]', '//div[@id="articleWrap"]', '//div[@id="divNewsContent"]', '//div[@class="article_content"]', '//div[@itemprop="articleBody"]']
    xpaths= np.array(xpaths)

    xpaths_s= list(xpaths.repeat(dupCnt))

    dictLink= dict(zip(link,xpaths_s))
    return dictLink
def mkDictNewsPress():
    """
    해당 링크가 어느 신문사인지
    """
    link= ['news.khan.co', 'www.khan.co', 'h2.khan.co', 'news.kmib.co', 'www.naeil.com', 'news.donga.com', 'www.donga.com', 'realestate.donga.com', 'bizn.donga.com', 'travel.donga.com', 'studio.donga.com', 'yachtpia.donga.com', 'it.donga.com', 'www.m-i.kr', 'www.munhwa.com', 'www.seoul.co', 'ntn.seoul.co', 'stv.seoul.co', 'www.segye.com', 'local.segye.com', 'www.segyefn.com', 'economysegye.segye.com', 'fn.segye.com', 'www.asiatoday.co', 'news.chosun.com', 'biz.chosun.com', 'car.chosun.com', 'life.chosun.com', 'businessnews.chosun.com', 'news.joins.com', 'realestate.joins.com', 'www.hani.co', 'babytree.hani.co', '2korea.hani.co', 'www.hankookilbo.com', 'www.newsis.com', 'sports.news.naver', 'news.naver.com', 'app.yonhapnews.co', 'www.wowtv.co', 'www.wownet.co', 'news.wowtv.co', 'sports.wowtv.co', 'wowstar.wowtv.co', 'news.jtbc.co', 'www.sisain.co', 'www.sisainlive.com']
    dupCnt= [3,1,1,8,1,1,3,5,1,5,2,3,1,2,2,5,1,2]
    press= ['경향신문', '국민일보', '내일신문', '동아일보', '매일일보', '문화일보', '서울신문', '세계일보', '아시아투데이', '조선일보', '중앙일보', '한겨레', '한국일보', '뉴시스', '연합뉴스', '한국경제TV ', 'JTBC', '시사IN']
    press= np.array(press)

    press_s= list(press.repeat(dupCnt))

    dictPress= dict(zip(link,press_s))
    return dictPress
dictLink= mkDictNewsXpath()
def whatLinksXpath(link):
    link3piece= '.'.join(link.split('/')[2].split('.')[0:3])
    xpath= dictLink[link3piece]
    return xpath
dictPress= mkDictNewsPress()
def whatLinksPress(link3piece):
    #link3piece= '.'.join(link.split('/')[2].split('.')[0:3])
    press= dictPress[link3piece]
    return press
def rmSpecialChr(weirdStr):
    """
    @param string
    @return string. #특문제거, \n -> ___
    """
    regPattLine= '\n'
    res= re.sub(regPattLine,'___',weirdStr)
    regPatt= '[^ㄱ-ㅎㅏ-ㅣ가-힣a-zA-Z0-9()": ]|[[\u3131-\u318E\uAC00-\uD7A3]]'
    res= re.sub(regPatt,'',res)
    res= re.sub('\\s+', ' ', res) # 공백 제거 해,말아? 하자. 안 하면 헬일듯
    return res
def getContent(link):
    """
    @return conBodyText
    """
    xpathBody= whatLinksXpath(link)
    #print(xpathBody)
    
    try:
        conBody= WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, xpathBody))
        )
        conBodyText= rmSpecialChr(conBody.text)
    except Exception as e:
        print('no match xpath',e)
        conBodyText= ""
        pass
    
    return conBodyText


if not os.path.exists('data'):
    mkdir("data")
    
# driver.close()
# driver.quit()
# TEST: link list from page-1
driver= startWeb()
searchOptPress()
numPage= 1
movePage(numPage)
listLink= list([])
listLink= saveLink(listLink)

listLink
driver.close()
driver.quit()
# TEST: news content from link-1
driver= startWeb()
searchOptPress()
# numPage= 2
# movePage(numPage)
dictLink= mkDictNewsXpath() # 최초 1번만 만들면 된다

linkEx= 'http://www.newsis.com/view/?id=NISX20180421_0000288016&cID=10803&pID=10800'
movePageLink(linkEx)
contents= getContent(linkEx)
contents

## Run
driver= startWeb()
searchOptPress()
# data/naverNewsSomePressLinks.csv 에 저장 완료!
numPages= range(1,400)
listLink= list([])

for numPage in numPages:
    print(numPage)
    movePage(numPage)
    listLink= saveLink(listLink)

print(len(listLink))
listLink
driver.close()
driver.quit()
# scraping 직후. 옵션외 링크가 좀 섞여있다
DataFrame(listLink).to_csv("data/naverNewsSomePressLinks.csv", index= False, header=None)
linkRead= pd.read_csv("data/naverNewsSomePressLinks.csv", header=None)

linkRead= list(linkRead[0])

print(len(linkRead))

linkRead[30:35]
df= DataFrame(linkRead)

exceptList= ['www.kukinews.com', 'news.kukinews.com', 'www.seouland.com', 'nownews.seoul.co', 'nownewstv.seoul.co', 'www.sporbiz.co', 'www.beautyhankook.com']
for exLink in exceptList:
    df= df[df[0].map(lambda x: (exLink not in x))]
    
print(len(df))

## 읽기- 광고 제거된 링크 목록
df.to_csv("data/naverNewsDailyPlusPressLinks.csv", index= False, header=None)
linkNewsDailyPlus= pd.read_csv('data/naverNewsDailyPlusPressLinks.csv',
                               header=None)

print(linkNewsDailyPlus.shape)
print(type(linkNewsDailyPlus[0]))
linkNewsDailyPlus.head(3)
linkNewsDailyPlus_list= list(linkNewsDailyPlus[0])
len(linkNewsDailyPlus_list)
driver.close()
driver.quit()

## 실행- 내용 얻기
linkNewsDailyPlus= pd.read_csv('data/naverNewsDailyPlusPressLinks.csv',
                               header=None)
linkNewsDailyPlus_list= list(linkNewsDailyPlus[0])
print(len(linkNewsDailyPlus_list))

bodyList= list([])
pressList3pie= list([])

dictLink= mkDictNewsXpath() # 최초 1번만 만들면 된다. driver와 무관
driver= startWeb()
searchOptPress()

for i, link in enumerate(linkNewsDailyPlus_list):
    #if (0== i)| (1==i):
    #print(link)
    print(i)

    movePageLink(link)
    body= getContent(link)
    bodyList.append(body)

    link3piece= '.'.join(link.split('/')[2].split('.')[0:3])
    pressList3pie.append(link3piece)
newsData= {
    'link3pie': pressList3pie,
    'zbody':bodyList
}
dfNews= pd.DataFrame(data= newsData)
dfNews.to_csv('data/naverNewsContent.csv', index= False, encoding= 'cp949')

dictPress= mkDictNewsPress()
dfNews['link3pie'].map(whatLinksPress).value_counts()
list(dfNews['link3pie'].map(whatLinksPress).unique())
dfNews['link3pie'].value_counts()
dfNC= pd.read_csv("data/naverNewsContent.csv", encoding= 'cp949')
dfNC.columns

## 기사중에서 특정 문자열 찾기
def findStr(inputStr):
    tradein= lambda x:inputStr in x
    return df[df.zbody.map(tradein)]

inputStr= '음식'
findStr(inputStr).to_csv('data/newsfind'+inputStr+'.csv', index= False, encoding= 'cp949')
