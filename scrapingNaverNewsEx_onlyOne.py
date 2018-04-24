# coding: utf-8
# coding: utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os.path
from os import rename
from os import listdir

import time

import csv

import pandas as pd
import numpy as np
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
def whatLinksXpath(link):
    link3piece= '.'.join(link.split('/')[2].split('.')[0:3])
    xpath= dictLink[link3piece]
    return xpath
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
    print(xpathBody)
    
    try:
        conBody= WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, xpathBody))
        )
        conBodyText= rmSpecialChr(conBody.text)
    except Exception as e:
        print('no match xpath',e)
        conBodyText= ""
        pass
    
    return conBodyText
driver.close()
driver.quit()
# WELL-DONE !
driver= startWeb()
searchOptPress()
numPage= 2
movePage(numPage)
dictLink= mkDictNewsXpath() # 최초 1번만 만들면 된다

linkEx= 'http://www.newsis.com/view/?id=NISX20180421_0000288016&cID=10803&pID=10800'
movePageLink(linkEx)
contents= getContent(linkEx)
contents
