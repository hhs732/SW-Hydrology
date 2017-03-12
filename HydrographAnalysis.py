# *************************************************************************************** #
# Hydrograph analysis for two watersheds of Sagehen Creek,CA and Happy Isles, Yosemite, CA.
# *************************************************************************************** #
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import datetime as dt
#%%
# **************************** Data Preparation ***************************** #
SagehenMaurer = pd.read_csv('010343500_lump_maurer_forcing_leap.txt',skiprows=3,delim_whitespace=True)
SagehenStreamflow = pd.read_csv('010343500_streamflow_qc.txt',delim_whitespace=True,names=['ID','Year','Mnth','Day','Q','Code'])
HappyMaurer = pd.read_csv('011264500_lump_maurer_forcing_leap.txt',skiprows=3,delim_whitespace=True)
HappyStreamflow = pd.read_csv('011264500_streamflow_qc.txt',delim_whitespace=True,names=['ID','Year','Mnth','Day','Q','Code'])

DateDF = SagehenMaurer[['Year','Mnth','Day']]
DateDF['Date'] = DateDF[DateDF.columns[0:]].apply(lambda x: ''.join(x.dropna().astype(int).astype(str)),axis=1)
DateDF['Date'] = pd.to_datetime((DateDF.Year*10000+DateDF.Mnth*100+DateDF.Day).apply(str),format='%Y%m%d')
SagehenMaurer.index = DateDF['Date']
HappyMaurer.index = DateDF['Date']

DateDF = SagehenStreamflow[['Year','Mnth','Day']]
DateDF['Date'] = DateDF[DateDF.columns[0:]].apply(lambda x: ''.join(x.dropna().astype(int).astype(str)),axis=1)
DateDF['Date'] = pd.to_datetime((DateDF.Year*10000+DateDF.Mnth*100+DateDF.Day).apply(str),format='%Y%m%d')
SagehenStreamflow.index = DateDF['Date']
HappyStreamflow.index = DateDF['Date']

SagehenMaurer2 = SagehenMaurer['1980-10-01':'2008-09-30']
SagehenStreamflow2 = SagehenStreamflow['1980-10-01':'2008-09-30']
HappyMaurer2 = HappyMaurer['1980-10-01':'2008-09-30']
HappyStreamflow2 = HappyStreamflow['1980-10-01':'2008-09-30']
#%%
# ********* Calculating Unit Streamflow/Precipitation (Q/P) ***************** #
SagehenArea = 27.34 * 1000000
HappyArea = 472.3 * 1000000

SagehenUnitQ = SagehenStreamflow2 ['Q']/SagehenArea
SagehenPrecipM = SagehenMaurer2 ['PRCP(mm/day)']/1000
HappyUnitQ = HappyStreamflow2 ['Q']/HappyArea
HappyPrecipM = HappyMaurer2 ['PRCP(mm/day)']/1000
                            
SagehenQovrP = SagehenUnitQ / SagehenPrecipM
SagehenQovrP[np.isinf(SagehenQovrP)]=0
SagehenQovrP = pd.Series(SagehenQovrP,name='QovrP')
HappyQovrP = HappyUnitQ / HappyPrecipM
HappyQovrP[np.isinf(HappyQovrP)]=0
HappyQovrP = pd.Series(HappyQovrP,name='QovrP')
#%%
# ***************** Average P/Q for each water year ************************* #
GroupMeanSegQP = SagehenQovrP.groupby(SagehenQovrP.index.year).mean() #Each Year
GroupMeanHapQP = HappyQovrP.groupby(HappyQovrP.index.year).mean() #Each Year

Year = SagehenQovrP.index.year
Month = SagehenQovrP.index.month
Day = SagehenQovrP.index.day

SagMeanYearWaterQovrP = []
j = 0 
for i in range(len(SagehenQovrP)):
    if SagehenQovrP.index.month[i] == 9 and SagehenQovrP.index.day[i] ==30 and SagehenQovrP.index.hour[i] == 0 and SagehenQovrP.index.minute[i] == 0 :
        SagMeanYearWaterQovrP.append(np.mean(SagehenQovrP[j:i]))

HapMeanYearWaterQovrP = []
for i in range(len(SagehenQovrP)):
    if HappyQovrP.index.month[i] == 9 and HappyQovrP.index.day[i] ==30 :
        HapMeanYearWaterQovrP.append(np.mean(HappyQovrP[0:i]))
#%%
# ********************** Flow Duration Curve ******************************** #
SagFlowSorted = SagehenStreamflow2.sort_values(['Q'])[::-1]
SagFlowSortedDrop = SagFlowSorted.drop(SagFlowSorted.columns[[0, 1, 2, 3, 5]], axis=1)
HapFlowSorted = HappyStreamflow2.sort_values(['Q'])[::-1]
HapFlowSortedDrop = HapFlowSorted.drop(SagFlowSorted.columns[[0, 1, 2, 3, 5]], axis=1)

SagRankFlow = SagFlowSortedDrop.rank(ascending=False) #scistat.rankdata(SagFlowSortedDrop,method='max')[::-1]
HapRankFlow = HapFlowSortedDrop.rank(ascending=False)
#HapRankFlow = pd.DataFrame(HapRankFlow, columns = ['RankForData'])

SagProbExcFlow = SagRankFlow/(1+np.size(SagFlowSortedDrop['Q']))
HapProbExcFlow = HapRankFlow/(1+np.size(HapFlowSortedDrop))

fig1 = plt.figure()
plt.plot(SagProbExcFlow, SagFlowSortedDrop['Q'])
fig1.autofmt_xdate()
plt.title('Flow Duration Curve for Sagehen')
plt.xlabel('Probability of Exceedance')
plt.ylabel('Sorted Streamflow')
plt.xticks(np.arange(0, 1, 0.1))
plt.savefig('SagehenFlowDurationCurve.png')

fig1 = plt.figure()
plt.plot(HapProbExcFlow, HapFlowSortedDrop['Q'])
fig1.autofmt_xdate()
plt.title('Flow Duration Curve for Happy')
plt.xlabel('Probability of Exceedance')
plt.ylabel('Sorted Streamflow')
plt.xticks(np.arange(0, 1, 0.1))
plt.savefig('HappyFlowDurationCurve.png')

SagRankEPFlow = np.column_stack((SagProbExcFlow, SagFlowSortedDrop))
SagRankEPFlowDF = pd.DataFrame(SagRankEPFlow, columns = ['PEX', 'Q'])
HapRankEPFlow = np.column_stack((HapProbExcFlow, HapFlowSortedDrop)) 
HapRankEPFlowDF = pd.DataFrame(HapRankEPFlow, columns = ['PEX', 'Q'])       

#IndexPEXAll = np.where(SagRankEPFlowDF.PEX == SPEX)
#IndexPEX = np.min (IndexPEXAll)
#FlowPEXS = np.array(SagRankEPFlowDF['Q'][IndexPEX])
SPEX = 0.9
for k in range (len(SagRankEPFlowDF ['PEX'])):
    if SPEX == SagRankEPFlowDF.PEX [k] :
        FlowPEXS = np.array(SagRankEPFlowDF['Q'][k])
        SagFlowPEX = np.mean(FlowPEXS)
        break
Holder1 = []
for k in range (len(SagRankEPFlowDF ['PEX'])):
    Holder1.append(SagRankEPFlowDF.PEX [k]-SPEX)
    Holder2 = min (Holder1, key=lambda x:abs(x))
    HolderPEX = Holder2 + SPEX
    IndexPEX = SagRankEPFlowDF.PEX[SagRankEPFlowDF.PEX == HolderPEX].index.tolist()
    FlowPEXS = np.array(SagRankEPFlowDF['Q'][IndexPEX])
    MeanFlowPEXS = np.mean(FlowPEXS)
if HolderPEX < SPEX :
    MaxIndexPEX = max (IndexPEX, key=lambda y:abs(y))+1
    FlowPELGS = np.array(SagRankEPFlowDF['Q'][MaxIndexPEX])
    SagFlowPEX = (MeanFlowPEXS + FlowPELGS)/2
elif HolderPEX > SPEX :
    MinIndexPEX = min (IndexPEX, key=lambda y:abs(y))-1
    FlowPELLS = np.array(SagRankEPFlowDF['Q'][MinIndexPEX])
    SagFlowPEX = (MeanFlowPEXS + FlowPELLS)/2
#%%
# ********************** Calculating Baseflow Index ************************* #
B = 0.925
q = np.zeros (len(SagehenStreamflow2['Q'])+1)
Q = SagehenStreamflow2 ['Q'].tolist()
Q.insert(0, 0)
for z in range (len(SagehenStreamflow2['Q'])):
    q[z +1] = (B * q[z]) + ((Q[z+1] - Q[z]) * ((1+B)/2))

q = [0 if x<0 else x for x in q]        
b = np.zeros((len (q)))
for i in range (len (q)):
    b [i] = Q [i] - q [i]   

DateAxis = SagehenStreamflow2.index
fig1 = plt.figure()
plt.plot(DateAxis, Q [1 : 10228])
plt.plot(DateAxis, b [1 : 10228])
fig1.autofmt_xdate()
plt.title('Hydrograph Analysis for Sagehen')
plt.xlabel('Time')
plt.ylabel('Flow')
plt.savefig('Hydrograph Analysis for Sagehen.png')

BaseFlowVol = b * 24 * 3600
QVol = Q * 24 * 3600
SumBaseFlowVol = sum (BaseFlowVol)
SumStreamFlowVol = sum (QVol)
BaseFlowIndex = SumStreamFlowVol / SumBaseFlowVol









































