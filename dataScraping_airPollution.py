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

def setDownPath():
    """
    @return chrome_options
    """
    saveDir= 'data' if ('data' in listdir('.')) else ""
    downPath= (os.path.abspath('.')+'\\'+saveDir).replace('\\','/')    
    options= webdriver.ChromeOptions() 
    prefs= {"download.default_directory": downPath}
    options.add_experimental_option("prefs",prefs)
    
    return options

def startWeb():
    """
    @return driver
    """
    options= setDownPath()
    driver= webdriver.Chrome('lib/chromedriver.exe', chrome_options= options)
    url= "http://cleanair.seoul.go.kr/air_pollution.htm?method=period"
    driver.get(url)
    
    return driver

def set_input(xpath_id, sendKeys):
    myXpath= '//input[@id="'+xpath_id+'"]'
    element= driver.find_element_by_xpath(myXpath)
    element.clear()
    element.send_keys(sendKeys)

def set_input_year(year):
    set_input("measure_cal1", year)
    set_input("measure_cal2", year)

def clickSearchBtn(driver):
    element= driver.find_element_by_xpath('//p[@class="schBtn1"]')
    element.click()

def clickExcelDownBtn(driver):
    try:
        element= WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//span[@class="exl_btn"]/a'))
        )
    except Exception as e:
        print('error',e)

    element.click()
    time.sleep(4)

def renameDownFile(year):
    for filename in listdir('data/'):
        if EXCEL_FILENAME == filename:
            rename('data/'+filename, 'data/'+year+'_airPollution.htm')
driver= startWeb()

EXCEL_FILENAME= "ExcelData.xls"

years= ["2016", "2017"]
for year in years:
    set_input_year(year)
    clickSearchBtn(driver)
    clickExcelDownBtn(driver)
    renameDownFile(year)
    
driver.close()
driver.quit()
