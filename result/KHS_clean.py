
# coding: utf-8

# In[102]:


import numpy as np
import pandas as pd
import xlrd
import openpyxl
from bs4 import BeautifulSoup


# In[103]:


file = pd.ExcelFile('C:/github/proj_sponge_bicycle/data/bicycleRental_tot_NANfloat.xlsx')


# In[104]:


table = file.parse('rent1617')


# In[105]:


table.head()


# In[106]:


table_2016 = table.ix[:99828,];table_2016.tail()


# In[107]:


table_2017 = table.ix[99829:,];table_2017.head()


# In[108]:


table_2016 = pd.DataFrame(table_2016, columns = ['area', 'rentcnt']);table_2016.head()


# In[109]:


sum_2016 = table_2016.groupby('area').sum();sum_2016.head()


# In[110]:


table_2017 = pd.DataFrame(table_2017, columns = ['area', 'rentcnt']);table_2017.head()


# In[111]:


sum_2017 = table_2017.groupby('area').sum();sum_2017.head()


# In[112]:


sum_2016


# In[113]:


new_area = ['Gwangjin-gu', 'Dongdaemun-gu', 'Mapo-gu', 'Seodaemun-gu', 'Seongdong-gu', 'Yangcheon-gu',
           'Yeongdeungpo-gu_1_', 'Yongsan-gu', 'Eunpyeong-gu', 'Jongno-gu', 'Jung-gu']


# In[114]:


sum_2016['new_area'] = new_area


# In[115]:


sum_2016 = pd.DataFrame(sum_2016, columns = ['new_area', 'rentcnt'])


# In[116]:


sum_2016 = sum_2016.reset_index('area').ix[:,1:]


# In[117]:


pd.DataFrame(sum_2016, columns = ['new_area', 'rentcnt'])


# In[118]:


svg = open('C:/Users/kitcoop/Desktop/Seoul_districts.svg', 'r').read()


# In[119]:


senior_count = {}
counts_only = []
min_value = 100;max_value = 0;past_header = False
for row in sum_2016:
    if not past_header:
        past_header = True
        continue

    try:
        unique = row[0]
        count = float(row[1].strip())
        senior_count[unique] = count
        counts_only.append(count)
    except:
        pass


# In[120]:


soup = BeautifulSoup(svg, 'xml')


# In[121]:


paths = soup.findAll('path')


# In[122]:


colors = ["#F1EEF6", "D489DA", "#C994c7", "#DF65B0", "#DD1C77", "#980043"]


# In[123]:


path_style = 'font-size:12px;fill-rule:nonzero;stroke:#FFFFFF;stroke-opacity:1;stroke-width:0.1;stroke-miterlimit:4;stroke-dasharray:none;stroke-linecap:butt;marker-start;none;stroke-linejoin:bevel;fill;'


# In[124]:


for p in paths:
    if p['id']:
        try:
            count = senior_count[p['id']]
        except:
            continue

    if count>250000:
        color_class = 5
    elif count>200000:
        color_class = 4
    elif count>150000:
        color_class = 3
    elif count>100000:
        color_class = 2
    elif count>50000:
        color_class = 1
    else:
        color_class = 0

    color=colors[color_class]
    p['style']=path_style+color

print(soup.prettify())

