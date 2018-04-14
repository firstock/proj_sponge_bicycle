## coding: utf-8
## http://aws.seoul.go.kr/Report/RptWeatherMonth.asp
import pandas as pd
from bs4 import BeautifulSoup
import re
import numpy as np
from pandas import DataFrame, Series

from datetime import datetime
from os import listdir
from os.path import isfile

def getNewidx(table):
    ta3dateTag= table[3].findAll('td',{'class': re.compile('RL[12]')})
    tab3= [ta3dateTag[i].getText() for i in range(len(ta3dateTag))]
    newidx= [datetime.strptime(x, '%y-%m-%d') for x in tab3]
    return newidx

def getContents(table):
    tab4RL12= table[4].findAll('td',{'class':re.compile('RL[12]')})
    ta4cellLen= len(tab4RL12)
    tab4cells= [tab4RL12[i].get_text() for i in range(ta4cellLen)]
    contents= DataFrame(np.array(tab4cells).reshape(-1,15)).iloc[:,:-2]
    return contents

def table4toDf(table):
    contents= getContents(table)
    newidx= getNewidx(table)
    NEWCOL= ['평균풍속', '평균풍향', '최대풍속', '최대풍향', '순간최고풍속'
         , '순간최고풍향', '기온평균', '기온최저', '기온최고', '강수일강수'
         , '습도평균', '습도최저', '습도최고']
    
    df= pd.DataFrame(np.array(contents), columns= NEWCOL)
    df.insert(0, column= '날짜', value= newidx)
    return df

def htm2df(filePath):
    soup= BeautifulSoup(open(filePath), 'html.parser')
    table= soup.find_all('table')
    df= table4toDf(table)
    return df

def getFilePathList(rootPath, folderOrder=0):
    """
    input: rootPath, #st folder
    return: filePathList[, folderCnt, fileCnt]
    """
    folderList= listdir(rootPath)
    folderCnt= len(folderList)
    fileCnt= len(listdir(rootPath+folderList[folderOrder]))
    
    allFileList= [[rootPath+folder+'/'+file for file in listdir(rootPath+folder)] for folder in folderList]
    
    return allFileList, folderCnt, fileCnt

def toNaN(df):
    """
    when, 1st column is no index. just column
    """
    f_nan= lambda x: x.replace('^-$','NaN', regex=True)
    #df.iloc[:,1:]= df.iloc[:,1:].apply(f_nan)
    df= df.apply(f_nan)
    return df


rootPath= 'data/weather/'
fileList, folderCnt, fileCnt= getFilePathList(rootPath)
# # 전체 칼럼
# for i in range(folderCnt):
#     df0= htm2df(fileList[i][0])
#     for j in range(fileCnt-1):
#         df1= htm2df(fileList[0][j+1])
#         df0= df0.merge(df1, how='outer')
        
#     df0= toNaN(df0.set_index('날짜'))
    
#     csvName= fileList[i][0].split('/')[-2]
#     df0.to_csv('data_join/'+csvName+'.csv', encoding='cp949')

# 일부 칼럼        
for i in range(folderCnt):
    df0= htm2df(fileList[i][0])[['날짜','평균풍속','최대풍속', '순간최고풍속', '기온평균', '강수일강수', '습도평균']]
    for j in range(fileCnt-1):
        df1= htm2df(fileList[0][j+1])[['날짜','평균풍속','최대풍속', '순간최고풍속', '기온평균', '강수일강수', '습도평균']]
        df0= df0.merge(df1, how='outer')
        
    df0= toNaN(df0.set_index('날짜'))
    
    csvName= fileList[i][0].split('/')[-2]
    df0.to_csv('data_join/'+csvName+'.csv', encoding='cp949')
