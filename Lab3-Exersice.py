#Make a clearly labeled graph of just the average daily discharge of the snow season (November-April) 
#for Sagehen using the techniques we learned in the lab. Turn in the graph as a .png file. 
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt 
import matplotlib.dates as mdates

sagehen = pd.read_csv('sagehendischarge.csv',skiprows=29,parse_dates=True)

sagehen_discharge = pd.DataFrame(sagehen['14n'])
sagehen_discharge.columns = ['Mean Discharge (m3/s)']
sagehen_discharge.set_index(pd.DatetimeIndex(sagehen['20d']),inplace=True) 

SagehenSnow = sagehen_discharge['2015-11-01':'2016-04-30']

Dates = pd.date_range(dt.datetime(2015,11,1),dt.datetime(2016,4,30))
plt.plot(Dates, SagehenSnow['Mean Discharge (m3/s)'])

hfmt = mdates.DateFormatter('%Y-%m-%d')

fig = plt.figure()
ax = fig.add_subplot(111)

ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax.xaxis.set_major_formatter(hfmt)

plt.plot(Dates, SagehenSnow['Mean Discharge (m3/s)'])

fig.autofmt_xdate()

plt.title('Average Daily Discharge of the Snow Season for Sagehen, CA in Water Year 2016')
plt.xlabel('Date')
plt.ylabel('Average Daily Discharge (m^3/s)')

plt.savefig('SagehenSnow.png')















