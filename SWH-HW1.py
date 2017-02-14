import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as scistat
#import matplotlib.dates as mdates

#### A)
#Create an array for the water years, then create two plots. 
#One with the water year on the x axis and the Maximum Daily Precipitation on the y axis 
#and one with the water year on the x axis and the Maximum Monthly Precipitation on the y axis.
#Label the axes and create a title for both graphs.

PrecipitationData = pd.read_csv('independencelake.csv')
Dates = pd.DataFrame(PrecipitationData['Water Year'])
PrecipDataCol = np.column_stack([PrecipitationData['Max Daily Precip (mm)'],PrecipitationData['Max Monthly Precip (mm)']])
PrecipDataFrame = pd.DataFrame(PrecipDataCol,columns=['Max Daily Precip (mm)','Max Monthly Precip (mm)'])
PrecipDataFrame.set_index([Dates['Water Year']],inplace=True)
#print(PrecipDataFrame)

fig1 = plt.figure()
plt.plot(Dates, PrecipDataFrame['Max Daily Precip (mm)'])
fig1.autofmt_xdate()
plt.title('Max Daily Precipitation (mm) from 1979 to 2017')
plt.xlabel('Year')
plt.ylabel('Max Daily Precip (mm)')
plt.xticks(np.arange(min(Dates['Water Year']), max(Dates['Water Year']), 3))
plt.savefig('MaxDailyPrecip.png')

fig2 = plt.figure()
plt.plot(Dates, PrecipDataFrame['Max Monthly Precip (mm)'])
fig2.autofmt_xdate()
plt.title('Max Monthly Precipitation (mm) from 1979 to 2017')
plt.xlabel('Year')
plt.ylabel('Max Monthly Precip (mm)')
plt.xticks(np.arange(min(Dates['Water Year']), max(Dates['Water Year']), 3))
plt.savefig('MaxMonthlyPrecip.png')

#%%
#### B) 
#Create four new variables. One will have the dataframe sorted by Maximum Daily
#Precipitation in ascending order, one will have the dataframe sorted by Maximum
#Monthly Precipitation in ascending order, one will have the dataframe sorted by
#Maximum Daily Precipitation in descending order, and one will have the dataframe
#sorted by Maximum Monthly Precipitation in descending order.

MaxDayPrecipAscend = PrecipDataFrame.sort_values(['Max Daily Precip (mm)'])
MaxDayPrecipAscend = MaxDayPrecipAscend.drop('Max Monthly Precip (mm)', axis=1)
MaxDayPrecipDescend = PrecipDataFrame.sort_values(['Max Daily Precip (mm)'])[::-1]
MaxDayPrecipDescend = MaxDayPrecipDescend.drop('Max Monthly Precip (mm)', axis=1)
MaxMonPrecipAscend = PrecipDataFrame.sort_values(['Max Monthly Precip (mm)'])
MaxMonPrecipAscend = MaxMonPrecipAscend.drop('Max Daily Precip (mm)', axis=1)
MaxMonPrecipDescend = PrecipDataFrame.sort_values(['Max Monthly Precip (mm)'])[::-1]
MaxMonPrecipDescend = MaxMonPrecipDescend.drop('Max Daily Precip (mm)', axis=1)

#%%
#### C) 
#Determine the ranks for the Maximum Daily and Maximum Monthly Precipitation
#values.Create a new variable for each of your arrays with ranked data.

RankMaxDayPrecip = scistat.rankdata(MaxDayPrecipAscend,method='average')
RankMaxMonPrecip = scistat.rankdata(MaxMonPrecipAscend,method='average')
RankDayPrecip = scistat.rankdata(PrecipDataFrame['Max Daily Precip (mm)'],method='average')
RankMonPrecip = scistat.rankdata(PrecipDataFrame['Max Monthly Precip (mm)'],method='average')

#%%
#### D) 
#Calculate the probability of exceedance for each of the values in your two 
#arrays with ranked data. The formula for probability of exceedance is:
#rank / (total number of values + 1)

ProbExcRankDayP = RankMaxDayPrecip/40
ProbExcRankMonP = RankMaxMonPrecip/40

#%%
#### E) 
#Make two plots. One for Daily Precipitation and one for Monthly Precipitation. 
#The plots should have the probability of exceedance on the x axis and the sorted
#precipitation values in descending order on the y axis. Label the axes and create
#a title for both graphs.

fig1 = plt.figure()
plt.plot(ProbExcRankDayP, MaxDayPrecipDescend['Max Daily Precip (mm)'])
fig1.autofmt_xdate()
plt.title('Probability of Exceedance for Max Daily Precipitation (mm)')
plt.xlabel('Probability of Exceedance')
plt.ylabel('Sorted Max Daily Precipitation (mm)')
plt.xticks(np.arange(0, 1, 0.1))
plt.savefig('ProbExcDailyPrecip.png')

fig1 = plt.figure()
plt.plot(ProbExcRankMonP, MaxMonPrecipDescend['Max Monthly Precip (mm)'])
fig1.autofmt_xdate()
plt.title('Probability of Exceedance for Max Monthly Precipitation (mm)')
plt.xlabel('Probability of Exceedance')
plt.ylabel('Sorted Max Monthly Precipitation (mm)')
plt.xticks(np.arange(0, 1, 0.1))
plt.savefig('ProbExcMonPrecip.png')

#%%
#### F)
#Find the return period for each probability of exceedance value. 
#The equation for the return period is:
#return period=1/probability of exceedance
ReturnPeriodDayP = 1/ProbExcRankDayP
ReturnPeriodMonP = 1/ProbExcRankMonP

#%%
#### G)
#Make two plots for the return periods for Daily and Monthly Precipitation. 
#These should have the return period on the x-axis and the sorted precipitation 
#values in descending order on the y-axis. 

fig1 = plt.figure()
plt.plot(ReturnPeriodDayP, MaxDayPrecipDescend['Max Daily Precip (mm)'])
plt.title('Return Period for Max Daily Precipitation (mm)')
plt.xlabel('Return Period (Year)')
plt.ylabel('Sorted Max Daily Precipitation (mm)')
plt.xticks(np.arange(0, max(ReturnPeriodDayP), 2))
plt.savefig('ReturnPerDailyPrecip.png')

fig1 = plt.figure()
plt.plot(ReturnPeriodMonP, MaxMonPrecipDescend['Max Monthly Precip (mm)'])
plt.title('Return Period for Max Monthly Precipitation (mm)')
plt.xlabel('Return Period (Year)')
plt.ylabel('Sorted Max Monthly Precipitation (mm)')
plt.xticks(np.arange(0, max(ReturnPeriodMonP), 2))
plt.savefig('ReturnPerMonPrecip.png')

#%%
#### H)
#Do a linear interpolation and use it to estimate the Maximum Monthly 
#Precipitation for a ten year return period. Then, draw a horizontal line 
#corresponding that value in the Maximum Monthly Precipitation plot you made 
#in part a). For how to draw a horizontal line on a graph, see here:
#matplotlib.pyplot.plot((1975,2016),(x,x),'k-')
#where x is replaced by the value you found for the 10 year return period.
fig2 = plt.figure()
plt.plot(Dates, PrecipDataFrame['Max Monthly Precip (mm)'])
fig2.autofmt_xdate()
plt.title('Max Monthly Precipitation (mm) from 1979 to 2017')
plt.xlabel('Year')
plt.ylabel('Max Monthly Precip (mm)')
plt.xticks(np.arange(min(Dates['Water Year']), max(Dates['Water Year']), 3))
#plt.savefig('MaxMonthlyPrecip.png')

DescendMonPrecip = pd.DataFrame(MaxMonPrecipDescend['Max Monthly Precip (mm)'])
DescendMonPrecip.set_index(ReturnPeriodMonP,inplace=True)
PrecipMonT10 = DescendMonPrecip['Max Monthly Precip (mm)'][10]
plt.plot((1975,2016),(PrecipMonT10,PrecipMonT10),'k-')

fig1 = plt.figure()
plt.plot(ReturnPeriodMonP, MaxMonPrecipDescend['Max Monthly Precip (mm)'])
plt.title('Return Period for Max Monthly Precipitation (mm)')
plt.xlabel('Return Period (Year)')
plt.ylabel('Sorted Max Monthly Precipitation (mm)')
plt.xticks(np.arange(0, max(ReturnPeriodMonP), 2))
#plt.savefig('ReturnPerMonPrecip.png')
plt.plot((0,41),(PrecipMonT10,PrecipMonT10),'k-')


#%%
DescendDayPrecipCol = np.column_stack([ReturnPeriodDayP,MaxDayPrecipDescend['Max Daily Precip (mm)']])
DescendDayPrecip = pd.DataFrame(DescendDayPrecipCol,columns=['Return Period','Sorted Daily Precip (mm)'])

DescendMonPrecipCol = np.column_stack([ReturnPeriodMonP,MaxMonPrecipDescend['Max Monthly Precip (mm)']])
DescendMonPrecip2 = pd.DataFrame(DescendMonPrecipCol,columns=['Return Period','Sorted Monthly Precip (mm)'])

#for value in DescendMonPrecip['Return Period']:
#    if value==10:
#        PrecipT10 = value
























