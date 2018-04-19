# coding: utf-8
brOri= pd.read_csv('data_join/bicycleRental_knnImpu.csv',
                      encoding='cp949', parse_dates=['날짜'])
brOri.area= pd.Categorical(brOri.area).codes
print(type(brOri.area[0]))
print(type(brOri.날짜[0]))
brOri.head(2)
byr= brOri
byr["year"] = byr["날짜"].dt.year
byr["month"] = byr["날짜"].dt.month
byr["day"] = byr["날짜"].dt.day
byr["hour"] = byr["날짜"].dt.hour
byr["minute"] = byr["날짜"].dt.minute
byr["second"] = byr["날짜"].dt.second
byr["dayofweek"] = byr["날짜"].dt.dayofweek
# byr['날짜'].dt.year
brCol= list(brOri.columns); brCol
brLen= len(brCol); brLen
byRcols= ["year", "month", "day", "hour", "minute", "second", "dayofweek"]
colsLen= len(byRcols); colsLen
fig, axis= plt.subplots(int(colsLen/2)+1,2)
fig.set_size_inches(20,30)

for i in range(colsLen):
    #print(int(i/2), i%2)
    sns.barplot(data= brOri, x= byRcols[i], y='rentcnt',
                ax= axis[int(i/2)][i%2])
