# coding: utf-8
import pandas as pd
from bs4 import BeautifulSoup
import re
import numpy as np
from pandas import DataFrame, Series

from datetime import datetime
guu='gwangjin'
fyear= '2016'
fmon= '01'
filePath= 'data/weather/'+guu+'gu/'+guu+fyear+fmon+'.htm'
filePath

soup= BeautifulSoup(open(filePath), 'html.parser')

table= soup.find_all('table')
from IPython.display import Image
Image('img/table_struct.png')
newidxName= table[1].find_all('th')[1].getText().replace(' ','')
newidxName
repeat_colspan= [2,2,2,3,1,3] #일사, 일조 제외

cols_some= table[2].find_all('tr')[0].getText().strip().split('\n')[:-2]
cols1= np.array(cols_some).repeat(repeat_colspan)
cols1= list(cols1)

cols2= table[2].find_all('tr')[1].get_text().strip().split('\n')

# print('cols1',len(cols1))
# print('cols2',len(cols2))

newCol= [col1+col2 for (col1, col2) in zip(cols1, cols2)]
newCol
ta3dateTag= table[3].findAll('td',{'class': re.compile('RL[12]')})
ta3dateTag
# print(type(ta3dateTag[:]))
# print(type(ta3dateTag[0]))
# print(len(ta3dateTag))

tab3= [ta3dateTag[i].getText() for i in range(len(ta3dateTag))]
# tab3

newidx= [datetime.strptime(x, '%y-%m-%d') for x in tab3]
newidx
tab4RL12= table[4].findAll('td',{'class':re.compile('RL[12]')})

# print('15열씩 %.0f행, 총%d개'%(len(tab4RL12)/15,len(tab4RL12)))

ta4cellLen= len(tab4RL12)
tab4cells= [tab4RL12[i].get_text() for i in range(ta4cellLen)]

contents= DataFrame(np.array(tab4cells).reshape(31,15)).iloc[:,:-2]
contents
newidxName
newCol
newidx
contents
newidx
#contents.set_index(newidx) - set_index는 기존 칼럼으로 만드는거
pd.DataFrame(np.array(contents), index= newidx, columns= newCol)
