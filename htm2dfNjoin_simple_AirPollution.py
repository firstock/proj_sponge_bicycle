# coding: utf-8
import pandas as pd
from pandas import DataFrame

def rmMultiidx(htm):
    df= htm[0]
    firstLine= list(df.columns.get_level_values(1))
    df.columns= df.columns.get_level_values(0)
    
    return df

def insert1stToDf(df, line):
    df.loc[-1]= line
    df.index+= 1
    df.sort_index(inplace= True)
    df.columns
    
    return df

def rmBlank_index(df):
    f= lambda x: str.replace(x, ' ','')
    df.columns= df.columns.map(f)
    
    return df

def htm2dfSimple(year):
    table= pd.read_html('data/airPollution_'+year+'.htm', encoding="utf-8", skiprows=[0,2,3])
    df= rmMultiidx(table)
    df= insert1stToDf(df, firstLine)
    df= rmBlank_index(df)
    df= df.sort_values(by=['날짜'], ascending=True).reset_index(drop=True)
    df= df[df['측정소명']!='평균']
    
    return df
    
year_1st= "2016"
years= ["2017"]

df= htm2dfSimple(year_1st)
for year in years:
    df= df.merge(htm2dfSimple(year), how= 'outer')
df
