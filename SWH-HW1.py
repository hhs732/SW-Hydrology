#Plotting and Calculating Return Time for Daily and Monthly Max Precipitation.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as scistat
#from scipy.interpolate import interp1d

#### A)
#Plotting Maximum Daily and Monthly Precipitation.
PrecipitationData = pd.read_csv('independencelake.csv')
Dates = pd.DataFrame(PrecipitationData['Water Year'])
PrecipDataCol = np.column_stack([PrecipitationData['Max Daily Precip (mm)'],PrecipitationData['Max Monthly Precip (mm)']])
PrecipDataFrame = pd.DataFrame(PrecipDataCol,columns=['Max Daily Precip (mm)','Max Monthly Precip (mm)'])
PrecipDataFrame.set_index([Dates['Water Year']],inplace=True)

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
#Dataframe for sorted Maximum Daily and Monthly Precipitation in ascending and descending order.
MaxDayPAscend = PrecipDataFrame.sort_values(['Max Daily Precip (mm)'])
MaxDayPrecipAscend = MaxDayPAscend.drop('Max Monthly Precip (mm)', axis=1)
MaxDayPDescend = PrecipDataFrame.sort_values(['Max Daily Precip (mm)'])[::-1]
MaxDayPrecipDescend = MaxDayPDescend.drop('Max Monthly Precip (mm)', axis=1)
MaxMonPAscend = PrecipDataFrame.sort_values(['Max Monthly Precip (mm)'])
MaxMonPrecipAscend = MaxMonPAscend.drop('Max Daily Precip (mm)', axis=1)
MaxMonPDescend = PrecipDataFrame.sort_values(['Max Monthly Precip (mm)'])[::-1]
MaxMonPrecipDescend = MaxMonPDescend.drop('Max Daily Precip (mm)', axis=1)

#%%
#### C) 
#Ranks for the Maximum Daily and Monthly Precipitation.
RankMaxDayPrecip = scistat.rankdata(MaxDayPrecipAscend,method='average')
RankMaxMonPrecip = scistat.rankdata(MaxMonPrecipAscend,method='average')
RankDayPrecip = scistat.rankdata(PrecipDataFrame['Max Daily Precip (mm)'],method='average')
RankMonPrecip = scistat.rankdata(PrecipDataFrame['Max Monthly Precip (mm)'],method='average')

#%%
#### D) 
#Probability of Exceedance for each of the values in your two arrays with ranked data.
ProbExcRankDayP = RankMaxDayPrecip/(1+np.size(PrecipDataFrame['Max Daily Precip (mm)']))
ProbExcRankMonP = RankMaxMonPrecip/(1+np.size(PrecipDataFrame['Max Monthly Precip (mm)']))

#%%
#### E) 
#Plotting probability of exceedance for the sorted daily and monthly precipitation in descending order.
fig1 = plt.figure()
plt.plot(ProbExcRankDayP, MaxDayPrecipDescend['Max Daily Precip (mm)'])
fig1.autofmt_xdate()
plt.title('Probability of Exceedance for Max Daily Precipitation (mm) in descending order')
plt.xlabel('Probability of Exceedance')
plt.ylabel('Sorted Max Daily Precipitation (mm)')
plt.xticks(np.arange(0, 1, 0.1))
plt.savefig('ProbExcDailyPrecip.png')

fig1 = plt.figure()
plt.plot(ProbExcRankMonP, MaxMonPrecipDescend['Max Monthly Precip (mm)'])
fig1.autofmt_xdate()
plt.title('Probability of Exceedance for Max Monthly Precipitation (mm) in descending order')
plt.xlabel('Probability of Exceedance')
plt.ylabel('Sorted Max Monthly Precipitation (mm)')
plt.xticks(np.arange(0, 1, 0.1))
plt.savefig('ProbExcMonPrecip.png')

#%%
#### F)
#Return Period for daily and monthly Max precipitation. 
ReturnPeriodDayP = 1/ProbExcRankDayP
ReturnPeriodMonP = 1/ProbExcRankMonP

#%%
#### G)
#Plotting Return periods for Daily and Monthly Max Precipitation. 
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
#Maximum Monthly Precipitation for a ten year return time.
DescendMonPrecip = pd.DataFrame(MaxMonPrecipDescend['Max Monthly Precip (mm)'])
DescendMonPrecip.set_index(ReturnPeriodMonP,inplace=True)
PrecipMonRT10 = DescendMonPrecip['Max Monthly Precip (mm)'][10]

fig2 = plt.figure()
plt.plot(Dates, PrecipDataFrame['Max Monthly Precip (mm)'])
fig2.autofmt_xdate()
plt.title('Max Monthly Precipitation (mm) from 1979 to 2017')
plt.xlabel('Year')
plt.ylabel('Max Monthly Precip (mm)')
plt.xticks(np.arange(min(Dates['Water Year'])-1, 1+max(Dates['Water Year']), 3))
plt.plot((1976,2017),(PrecipMonRT10,PrecipMonRT10),'k-')
plt.savefig('RT10-MonPrecip.png')

fig1 = plt.figure()
plt.plot(ReturnPeriodMonP, MaxMonPrecipDescend['Max Monthly Precip (mm)'])
plt.title('Return Period for Max Monthly Precipitation (mm)')
plt.xlabel('Return Period (Year)')
plt.ylabel('Sorted Max Monthly Precipitation (mm)')
plt.xticks(np.arange(0, max(ReturnPeriodMonP), 3))
plt.plot((0,1+np.size(PrecipDataFrame['Max Monthly Precip (mm)'])),(PrecipMonRT10,PrecipMonRT10),'k-')

#%%
#Maximum Daily and Monthly Precipitation for specific return time.
DescMonPrecipCol = np.column_stack([ReturnPeriodMonP,MaxMonPrecipDescend['Max Monthly Precip (mm)']])
DescMonPrecip = pd.DataFrame(DescMonPrecipCol,columns=['ReturnTime','Sorted Monthly Precip (mm)'])

SPMonReturnTime = 10
for value in DescMonPrecip['ReturnTime']:
    if value==SPMonReturnTime:
        IndexRTimeM = DescMonPrecip.ReturnTime[DescMonPrecip.ReturnTime == value].index.tolist()
        IndexRtrnTimeM = np.array([float(i) for i in IndexRTimeM]) 
        PrecipMonRTE = np.array(DescMonPrecip['Sorted Monthly Precip (mm)'][IndexRtrnTimeM])
        PrecipMonRTL1 = np.array(DescMonPrecip['Sorted Monthly Precip (mm)'][IndexRtrnTimeM-1])
        PrecipMonRTM1 = np.array(DescMonPrecip['Sorted Monthly Precip (mm)'][IndexRtrnTimeM+1])
        PrecipMonRT = (PrecipMonRTE+PrecipMonRTL1+PrecipMonRTM1)/3
print (PrecipMonRT)

DescDayPrecipCol = np.column_stack([ReturnPeriodDayP,MaxDayPrecipDescend['Max Daily Precip (mm)']])
DescDayPrecip = pd.DataFrame(DescDayPrecipCol,columns=['ReturnTime','Sorted Daily Precip (mm)'])

Holder1 = []
SPDayReturnTime = 10
for value in DescDayPrecip['ReturnTime']:
#    print(value)
#    print(SPDayReturnTime)
    if value==SPDayReturnTime:
        IndexRTimeD = DescDayPrecip.ReturnTime[DescDayPrecip.ReturnTime == value].index.tolist()
        IndexRTimeDF = np.array([float(i) for i in IndexRTimeD]) 
        PrecipDayRT = DescDayPrecip['Sorted Daily Precip (mm)'][IndexRTimeDF]
        break                            
    else:
        Holder1.append(value-SPDayReturnTime)
        Holder2 = min (Holder1, key=lambda x:abs(x))
        IndexHolder1 = Holder2 + SPDayReturnTime
        if value == IndexHolder1: 
            IndexRTimeD = DescDayPrecip.ReturnTime[DescDayPrecip.ReturnTime == value].index.tolist()
            IndexRTimeDF = np.array([float(i) for i in IndexRTimeD])
            PrecipDayRTE = np.array(DescDayPrecip['Sorted Daily Precip (mm)'][IndexRTimeDF])
            #PrecipDayRTEMean = np.mean(PrecipDayRTE)
            PrecipDayRTL = np.array(DescDayPrecip['Sorted Daily Precip (mm)'][IndexRTimeDF-1])
            PrecipDayRTL1 =  max (PrecipDayRTL, key=lambda x:abs(x))
            PrecipDayRTM = np.array(DescDayPrecip['Sorted Daily Precip (mm)'][IndexRTimeDF+1])
            PrecipDayRTM1 = min (PrecipDayRTM, key=lambda x:abs(x))
            PrecipDayRT = (PrecipDayRTM1+PrecipDayRTL1+np.mean(PrecipDayRTE))/3

#        IntrpltRtrnTime = DescDayPrecip['ReturnTime']
#        IntrpltDayPrecip = DescDayPrecip['Sorted Daily Precip (mm)']
#        IntrpltFunction = interp1d(IntrpltRtrnTime, IntrpltDayPrecip)
#        PrecipDayRT = IntrpltFunction(SPDayReturnTime)
print (PrecipDayRT)























