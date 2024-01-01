import ephem #Calculations for TLE to longitude and latitude
import pandas as pd #For tme .csv file 

def isLunar(year):
    """Check if the given year is a lunar year or not"""
    if year % 4 ==0 and year % 100 !=0:
        return True
    elif year % 400 == 0:
        return True
    elif year % 100 == 0:
        return False
    else:
        return False

def format(data):
    """Formats the date/time so there is at least 2 digits"""
    if(len(str(data)) == 1):
        return "0"+str(data)
    return str(data)[0:2]

def calculateDate(date):
    """Calculates the date in 'YYYY/MM/DD hh/mm/ss' format given epoch time. Invalid for times beyond the frame of 1957 to 2026 (inclusive)."""
    lunarMonths = {0:'1',
             31:'2',
             60:'3',
             91:'4',
             121:'5',
             152:'6',
             182:'7',
             213:'8',
             244:'9',
             274:'10',
             305:'11',
             335:'12'}
             
    nonLunarMonths = {0:'1',
             31:'2',
             59:'3',
             90:'4',
             120:'5',
             151:'6',
             181:'7',
             212:'8',
             243:'9',
             273:'10',
             304:'11',
             334:'12'}
             
    #raw data from @param{date}
    year = int(date[0:2])
    day = int(date[2:5])
    time = int(date[6:])
    #The first year of the satellite is 1957, so any year bigger than this is in the 20th century 
    if(year>=57): 
        year+= 1900 
    else:
        year+= 2000 

    #Check if the year is a lunar year
    if(isLunar(year)):
        daysInMonth = list(lunarMonths.keys())
    else:
        daysInMonth = list(nonLunarMonths.keys())
    daysInMonth.append(367) #The max possible day is 366, so 367 is our marker for what is within the 12 month calendar
    month = ''
    for i in range(0,len(daysInMonth)-1):
        tempMonth1 = day-daysInMonth[i]
        tempMonth2 = day-daysInMonth[i+1]
        #The 2nd month overshot the date and is negative, thus the i-th month is the proper month. We can stop iterating when we find the proper month 
        if(tempMonth2 <= 0):
            if(isLunar(year)): 
                month = lunarMonths[daysInMonth[i]]
            else:
                month = nonLunarMonths[daysInMonth[i]]
            break
     
    day = tempMonth1 #The day is what remains from the difference taking the days up to that month away
   
    times = [] #hours, minutes, seconds, milliseconds
    
    times.append(time // (60*60*1000))
    time = time - times[0] * (60*60*1000)

    times.append(time // (60*1000))
    time = time - times[1] * (60*1000)
    
    times.append(time // (1000)) 
    time = time - times[2] * (1000)
    
    times.append(time)

    
    print(times)
    #print(f"{year}/{month}/{day} {time[0]}:{times[1]}:{times[2]}:{times[3]}")
    return f"{year}/{format(month)}/{format(day)} {format(times[0])}:{format(times[1])}:{format(times[2])}:{format(times[3])}"



#dataset = "/home/johnzhou/QMind/ISS-data-1998-11-20-to-2023-12-26.txt"
#csvOutput = "/home/johnzhou/QMind/ISS-converted.csv"
dataset = "/home/johnzhou/QMind/data-new.txt"
csvOutput = "/home/johnzhou/QMind/data-new-converted.csv"


data = open(dataset,'r')
lines = data.readlines()
count = 0
line1=""
line2=""
date=""
satelliteNumbers = []
dates = []
longitudes = []
latitudes = []

#iterate over every line in the file
for line in lines:
    if(count==0):
        line1 = line
        date = calculateDate(line1[18:33])
        satelliteNumber = line1[2:7]
    else:
        line2 = line
    count+=1
    if (count==2):
        iss = ephem.readtle(satelliteNumber,line1,line2)
        iss.compute(date)
        count = 0
        satelliteNumbers.append(satelliteNumber)
        dates.append(date)
        longitudes.append(iss.sublong)
        latitudes.append(iss.sublat)


#Put the data in a dataframe, which is put into a .csv file
csvData = pd.DataFrame({
    "SatelliteNumber": satelliteNumbers,
    "Date": dates,
    "Longitude": longitudes,
    "Latitude": latitudes
})

#Sort the elements by date:
#csvdata.sort_values(by="satellitenumber", inplace=true, kind='stable')
csvData.sort_values(by="SatelliteNumber", inplace=True, kind='stable')
csvData.sort_values(by="Date", inplace=True) 

#Sort the elements by the satellite number, doing it with 'stable' as 
#Stable retains the order of the dates.
csvData.sort_values(by="SatelliteNumber", inplace=True, kind='stable')

csvData.to_csv(csvOutput, index=False)


print(repr(iss.sublong))
print(repr(iss.sublat))
print(type(iss.sublong))
print(type(iss.sublat))
print(csvData)


"""Try it out on a single value (the very first line in the dataset file)"""
#Try out 1 value

line1 = "ISS (ZARYA)"
#line2 = "1 25544U 98067A   03097.78853147  .00021906  00000-0  28403-3 0  8652"
#line3 = "2 25544  51.6361  13.7980 0004256  35.6671  59.2566 15.58778559250029"

line2 = "1 25544U 98067A   00001.09674769  .00024919  00000-0  26729-3 0  9993"
line3 = "2 25544 051.5903 277.4914 0008140 028.2594 186.2890 15.63615809 63537"
iss = ephem.readtle(line1, line2, line3)

date = calculateDate(line2[18:33])
#iss.compute('2003/3/23 12:12:12:100')
print(date)
iss.compute(date)
print('%s %s' % (repr(iss.sublong), repr(iss.sublat)))#Note repr is the true angle in radians, without this function we get it in a different notation

