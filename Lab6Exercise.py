#Creating a Budyko plot
#######################
#The Hamon ET model 
#######################
import numpy as np
import pandas as pd
import datetime as dt
import math
import matplotlib.pyplot as plt
#%%
niwotdata=pd.read_csv('AMF_US-NR1_BASE_HH_8-1.csv',skiprows=2,parse_dates=True)
timestamp=np.array(niwotdata['TIMESTAMP_START'])
timestamp=pd.DataFrame(timestamp,columns=['DATETIME'])
timestamp['DATETIME']=timestamp['DATETIME'].apply(lambda x: pd.to_datetime(str((int(x))).strip(), format='%Y%m%d%H%M'))
#%%
Temp=niwotdata['TA']
WindSpeed=niwotdata['WS']
LEvel=niwotdata['LE']
NetRadiation=niwotdata['NETRAD']
AirPressure=niwotdata['PA']
delta_e=niwotdata['VPD_PI']
Precip=niwotdata['P']
#%%
newdf=np.column_stack([Temp, WindSpeed, LEvel, NetRadiation, AirPressure, delta_e, Precip])

newdf=pd.DataFrame(newdf,columns=['Temp', 'WindSpeed', 'LEvel', 'NetRadiation', 'AirPressure', 'delta_e', 'Precip'])
#Add the datetime column to your dataframe
newdf.set_index(pd.DatetimeIndex(timestamp['DATETIME']),inplace=True) 
#Selecting data that is from between October 1st 1999 and September 30th 2002. These are Water Years 2000-2002
WY2000to2002=newdf[dt.datetime(1999,10,1,0,0):dt.datetime(2002,9,30,0,0)]

WY2000to2002.to_csv('Lab6data.csv')
#%%
#Creating a series for the air temperature data (as a numpy array) that has the dates as an index 
wy1_airtemp=pd.Series(np.array(WY2000to2002['Temp']),index=WY2000to2002.index)
#Calculating the average monthly air temperature
MeanMonTemp=wy1_airtemp.resample("M").mean()
#%%
#Calculating the es values using the average monthly air temperature for each month
count=len(WY2000to2002['AirPressure'])
j=0
es=np.zeros(count)
T=np.zeros(count)
for i in range(len(WY2000to2002['AirPressure'])):
    if (WY2000to2002.index[i]==MeanMonTemp.index[j]):
        es[i]=6.108*np.exp((17.27*MeanMonTemp[j])/(MeanMonTemp[j]+237.3))
        T=MeanMonTemp[j]
        j=j+1
    else:
        es[i]=6.108*np.exp((17.27*MeanMonTemp[j])/(MeanMonTemp[j]+237.3))
        T=MeanMonTemp[j]
#%%
#Julian days function
def JulianDays(datetimes):
    yearlist=[]
    for i in range(len(datetimes)):
        tt=datetimes[i].timetuple()
        #tt_list=list(tt)
        yearlist.append(tt[-2])
    return yearlist

julianday=JulianDays(WY2000to2002.index)
julianday[-1]
#%%
#Calculating N (daytime length) through finding P and D
count2=len(WY2000to2002['AirPressure'])
P=np.zeros(count)
D=np.zeros(count)
N=np.zeros(count)
for i in range(len(julianday)):
    P[i] = math.asin(.39795*math.cos(.2163108+2*math.atan(.9671396*math.tan(.00860*(julianday[i]-186)))))
    L=39.578056
    D[i] = 24-(24/np.pi)*math.acos((math.sin(0.8333*math.pi/180) + math.sin(L*math.pi/180)*math.sin(P[i]) /(math.cos(L*math.pi/180)*math.cos(P[i]))))
    N[i]=D[i]/12

#Calculating PET using the N, es, and T arrays 
PET=1.2*0.165*216.7*N*(es/(T+273.3))
PETHamideh = PET
#Calculating the actual ET 
LE=np.array(WY2000to2002['LEvel'])
convfactor=((1./1000.)/2264.76)
ETactual=LE*convfactor
ETactual=ETactual*3600.*24.

#Dataframe for ET and PET 
ETandPET=pd.DataFrame(PET,columns=['PET'])
ETandPET.insert(0,'ET',ETactual)

#This makes sure that ET and PET are never below zero 
for i in range(len(ETandPET['ET'])):
    if (ETactual[i]<=0):
        ETactual[i]=0
    elif (PET[i]<=0):
        PET[i]=0

PET_ET=np.column_stack([PET,ETactual])
PET_ET_df=pd.DataFrame(PET_ET,columns=['PET','ET'])
#%%
#Ploting ET vs PET 
plt.figure(figsize=(10,10))
PET_ET_df.plot(kind='scatter',x='PET',y='ET')
axes = plt.gca()
axes.set_xlim([0,3.5])
axes.set_ylim([0,25])
#%%
Wy1_Precip=pd.Series(np.array(WY2000to2002['Precip']),index=WY2000to2002.index)
WYPrecip = np.array(WY2000to2002['Precip'])
MeanMonPrecip=Wy1_Precip.resample("M").mean()

DrynessIndex=np.zeros(len(Wy1_Precip))
for k in range (len(Wy1_Precip)):
    if WYPrecip[k] == 0 :
        DrynessIndex[k] = 0
    else:
        DrynessIndex[k] = PET[k]/WYPrecip[k]
EvaporativeIndex=np.zeros(len(Wy1_Precip))
for y in range (len(Wy1_Precip)):
    if WYPrecip[y] == 0 :
        EvaporativeIndex[y] = 0
    else:
        EvaporativeIndex[y] = ETactual[y]/WYPrecip[y]

#Ploting Budyko Curve 
fig1 = plt.figure()
plt.scatter(DrynessIndex, EvaporativeIndex)
plt.title('Budyko Curve')
plt.xlabel('DrynessIndex')
plt.ylabel('EvaporativeIndex')
plt.xticks(np.arange(min(DrynessIndex), max(DrynessIndex), 3))
#
#
#plt.figure(figsize=(10,10))
#PET_ET_df.plot(kind='scatter',x='PET',y='ET')
#axes = plt.gca()
#axes.set_xlim([0,3.5])
#axes.set_ylim([0,25])
#


































