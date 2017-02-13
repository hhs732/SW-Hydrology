import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import matplotlib.dates as mdates
#import scipy as sp

#### a)
#Create an array for the water years, then create two plots. 
#One with the water year on the x axis and the Maximum Daily Precipitation on the y axis 
#and one with the water year on the x axis and the Maximum Monthly Precipitation on the y axis.
#Label the axes and create a title for both graphs.

PrecipitationData = pd.read_csv('independencelake.csv')
Dates = pd.DataFrame(PrecipitationData['Water Year'])
PrecipDataCol = np.column_stack([PrecipitationData['Max Daily Precip (mm)'],PrecipitationData['Max Monthly Precip (mm)']])
PrecipDataFrame = pd.DataFrame(PrecipDataCol,columns=['Max Daily Precip (mm)','Max Monthly Precip (mm)'])
PrecipDataFrame.set_index([Dates['Water Year']],inplace=True)
print(PrecipDataFrame)

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
### b) 
#Create four new variables. One will have the dataframe sorted by Maximum Daily
#Precipitation in ascending order, one will have the dataframe sorted by Maximum
#Monthly Precipitation in ascending order, one will have the dataframe sorted by
#Maximum Daily Precipitation in descending order, and one will have the dataframe
#sorted by Maximum Monthly Precipitation in descending order.







































