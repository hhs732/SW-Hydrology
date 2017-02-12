#1.What are the following variable types?
#  a.	1
#  b.	3.5
#  c.	5.
#  d.	‘marshmallow’
#  e.	str(4000)
print (type(1))
print (type(3.5))
print (type(5.))
print (type('marshmallow'))
print (type(str(4000)))
#%%
#2. Save the following information in a Dictionary and then write the information into a .csv file. Attach the .csv file to your lab turn-in. 
#Time: 6,12,18
#Temperature: 18,20,15
#Weather: Sunny, Partly Cloudy, Cloudy
import csv
Weatherdict = {'Time': [6,12,8],'Temperature':[18,20,15],'Weather':['Sunny','Partly Cloudy','Cloudy']}
print(Weatherdict['Weather'][1])

with open('Lab2HWQ2.csv', 'w') as csvfile:
    fieldnames = ['Time', 'Temperature', 'Weather']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({'Time': 6, 'Temperature': 18, 'Weather': 'Sunny'})
    writer.writerow({'Time': 12, 'Temperature': 20, 'Weather': 'Partly Cloudy'})
    writer.writerow({'Time': 8, 'Temperature': 15, 'Weather': 'Cloudy'})
#%%
#3.	Open the file independencelake.csv in iPython. 
#Then, use a for loop and an if-else statement to find 
#what years had maximum daily streamflow values that 
#exceeded 100mm and store them in a list. 

#List = [56, 102, 76]
#print(List)
#WOW = []
#for value in List:
#    if value > 100:
#        WOW.append(value)
YEAR = []
DAILYPRECIP = []
with open(r'C:\UNR\Thesis\Hydrological Modeling\SW Hydrology\Lab2-Python1\Lab2-Python1\independencelake.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        #print (row['Water Year'])
        #print (row['Max Daily Precip (mm)'])
        YEAR.append(row['Water Year'])
        DAILYPRECIP.append(row['Max Daily Precip (mm)'])
#print(YEAR)
#print(DAILYPRECIP)

IntegerYear = []
IntegerPrecip = []    
for value0 in (DAILYPRECIP):
    IntegerPrecip.append(int(value0))
for value1 in (YEAR):
    IntegerYear.append(int(value1))

PreStorm = []
for value2 in (IntegerPrecip):
    if value2 > 100:
        PreStorm.append(value2)
print(PreStorm)
#%%
import numpy as np 
Year = np.array(IntegerYear)
Precip = np.array(IntegerPrecip)
PrecipMatrix = np.column_stack((Year, Precip))
#print (PrecipMatrix)
R = np.array(len(PrecipMatrix)) #39
C = np.array(len(PrecipMatrix.T)) #2
#Storm = np.empty((R,C))
#I am using "List" here, instead of "Matrix"
StormEmpty = []
for i in range (R):
    for j in range (C):
        if PrecipMatrix[i,1]>100 :
            StormEmpty.append(PrecipMatrix[i,j])
            #Storm[i,j] = PrecipMatrix
StormEmpty2 = []
for Value4 in StormEmpty:
    FloatValue = float (Value4)
    StormEmpty2.append(FloatValue)

PreStorm2 = np.array(StormEmpty2)
SizeStorm = np.size(PreStorm2)
Storm = np.reshape(PreStorm2,(9,2))
print (Storm)

import xlwt
Output = xlwt.Workbook()
SizeStorm = np.array(np.shape(Storm))
Sheet = Output.add_sheet('Storm')
Header = np.array(["Year","Preciptation>100mm"])
for p in range (SizeStorm[1]): 
    Sheet.write(0, p, Header[p])
NumFormat = xlwt.easyxf(num_format_str='0')
for p in range (SizeStorm[1]):
    for q in range (SizeStorm[0]):
        Sheet.write(q+1, p, Storm[q,p],NumFormat)
Output.save('Lab2HWQ3.xls')

Storm.tofile('Lab2HWQ3.csv',sep=',')
#%%    
#???????????????????
#with open('Lab2HWQ3.csv', 'w') as csvfile:
#    fieldnames = ['Year', 'Storm']
#    writer = csvfile.writer(Storm)#, fieldnames=fieldnames)
#    writer.writeheader()
#    writer.writerows(Storm)























