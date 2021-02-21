import datetime
import urllib.request
import shapefile as shp
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from bs4 import BeautifulSoup
from datetime import datetime as dt
from matplotlib import dates
from urllib.request import Request, urlopen


def day1():

    stations = open('ForecastPoints.csv')

    sections = []
    HighList = []
    LowList = []
    CityNames = []
    Latitude = []
    Longitude = []

    for line in stations:
        listify = line.split(',')
        x = listify[0]
        y = listify[1]
        city = listify[2]
        CityNames.append(city)
        office = listify[3]
        lat = eval(listify[4])
        Latitude.append(lat)
        lon = eval(listify[5])
        Longitude.append(lon)

        url = 'https://api.weather.gov/gridpoints/{0}/{1},{2}/forecast/'.format(office,x,y)
        html = urllib.request.urlopen(url)
        soup = BeautifulSoup(html,features='html.parser')

        massivestring = str(soup)

        bigsplit = massivestring.split('{')

        count = 0

        for i in bigsplit:
            if count > 5:
                sections.append(i)
            else:
                pass
            count = count + 1

        for i in sections:
            #if limit < 2:
            tostring = str(i)
            day1 = tostring.split('"isDaytime": ')
            day2 = str(day1[1])
            day3 = day2.split(',')
            Day = str(day3[0])

            number1 = tostring.split('"number": ')
            number2 = str(number1[1])
            number3 = number2.split(',')
            Number = eval(number3[0])
                
            if Number == 1:
                if Day == 'false':
                    pass
                else:
                    temp1 = tostring.split('"temperature": ')
                    temp2 = str(temp1[1])
                    temp3 = temp2.split(',')
                    Temp = eval(temp3[0])
                    HighList.append(Temp)

                    time1 = tostring.split('"startTime": "')
                    time2 = str(time1[1])
                    time3 = time2.split(':00-05:00",')
                    time4 = str(time3[0])
                    Time = dt.strptime(time4,'%Y-%m-%dT%H:%M')
            if Number == 2:
                if Day == 'false':
                    temp1 = tostring.split('"temperature": ')
                    temp2 = str(temp1[1])
                    temp3 = temp2.split(',')
                    Temp = eval(temp3[0])
                    LowList.append(Temp)
                else:
                    temp1 = tostring.split('"temperature": ')
                    temp2 = str(temp1[1])
                    temp3 = temp2.split(',')
                    Temp = eval(temp3[0])
                    HighList.append(Temp)

                    time1 = tostring.split('"startTime": "')
                    time2 = str(time1[1])
                    time3 = time2.split(':00-05:00",')
                    time4 = str(time3[0])
                    Time = dt.strptime(time4,'%Y-%m-%dT%H:%M')
            if Number == 3:
                if Day == 'false':
                    temp1 = tostring.split('"temperature": ')
                    temp2 = str(temp1[1])
                    temp3 = temp2.split(',')
                    Temp = eval(temp3[0])
                    LowList.append(Temp)
                else:
                    pass
        sections = []

    fig = plt.figure(figsize=(14,7))
    ax = plt.axes()

    ax.set(xlim=(-84.84, -74.85), ylim=(32.0, 36.8))
    plt.xlim(-84.84, -74.85)
    plt.ylim(32.0, 36.8)

    ax.axis('off')

    sf = shp.Reader("NC & SC Counties.shp")

    for shape in sf.shapeRecords():
        for i in range(len(shape.shape.parts)):
            i_start = shape.shape.parts[i]
            if i==len(shape.shape.parts)-1:
                i_end = len(shape.shape.points)
            else:
                i_end = shape.shape.parts[i+1]
            e = [i[0] for i in shape.shape.points[i_start:i_end]]
            f = [i[1] for i in shape.shape.points[i_start:i_end]]
            plt.plot(e,f, color='grey', linewidth=0.3)

    sf = shp.Reader("NC & SC State.shp")

    for shape in sf.shapeRecords():
        for i in range(len(shape.shape.parts)):
            i_start = shape.shape.parts[i]
            if i==len(shape.shape.parts)-1:
                i_end = len(shape.shape.points)
            else:
                i_end = shape.shape.parts[i+1]
            e = [i[0] for i in shape.shape.points[i_start:i_end]]
            f = [i[1] for i in shape.shape.points[i_start:i_end]]
            plt.plot(e,f, color='black', linewidth=0.5)

    font1 = {'fontname':'Candara','size':16,'color':'black','weight':'bold'}
    font2 = {'fontname':'Candara','size':24,'color':'black','weight':'bold'}
    font3 = {'fontname':'Candara','size':24,'color':'goldenrod','weight':'bold'}
    font4 = {'fontname':'Candara','size':24,'color':'royalblue','weight':'bold'}
    font5 = {'fontname':'Candara','size':22,'color':'black','weight':'bold'}
    zcount = 0
    for i,j in zip(Longitude, Latitude):
        plt.text(i-0.17,j-0.14,HighList[zcount],size=16,weight='bold',color='goldenrod',ha='center')
        plt.text(i+0.17,j-0.14,LowList[zcount],size=16,weight='bold',color='royalblue',ha='center')
        plt.text(i,j-0.14,'/',size=16,color='black',ha='center')
        plt.text(i,j+0.08,CityNames[zcount],ha='center',**font1)
        zcount = zcount + 1

    ForecastDay = Time.strftime('%A')
    ForecastDate = Time.strftime('%B %d, %Y')

    im = plt.imread('CWGLogo.png')
    newax = fig.add_axes([0.65, 0.13, 0.2, 0.2], anchor='SE', zorder=-1)
    newax.imshow(im)
    newax.axis('off')

    fig.text(0.5,0.94,'National Weather Service',ha='center',**font2)
    fig.text(0.3,0.88,'High',ha='center',**font3)
    fig.text(0.3375,0.88,'/',ha='center',**font2)
    fig.text(0.37,0.88,'Low',ha='center',**font4)
    fig.text(0.552,0.88,'Temperature Forecast',ha='center',**font2)
    fig.text(0.25,0.22,ForecastDay,ha='center',**font5)
    fig.text(0.25,0.18,ForecastDate,ha='center',**font5)
    
    plt.savefig("output/NWSForecast1.png", bbox_inches='tight', dpi=200)

day1()

def day2():

    stations = open('ForecastPoints.csv')

    sections = []
    HighList = []
    LowList = []
    CityNames = []
    Latitude = []
    Longitude = []

    for line in stations:
        listify = line.split(',')
        x = listify[0]
        y = listify[1]
        city = listify[2]
        CityNames.append(city)
        office = listify[3]
        lat = eval(listify[4])
        Latitude.append(lat)
        lon = eval(listify[5])
        Longitude.append(lon)

        url = 'https://api.weather.gov/gridpoints/{0}/{1},{2}/forecast/'.format(office,x,y)
        html = urllib.request.urlopen(url)
        soup = BeautifulSoup(html,features='html.parser')

        massivestring = str(soup)

        bigsplit = massivestring.split('{')

        count = 0

        for i in bigsplit:
            if count > 5:
                sections.append(i)
            else:
                pass
            count = count + 1

        for i in sections:
            #if limit < 2:
            tostring = str(i)
            day1 = tostring.split('"isDaytime": ')
            day2 = str(day1[1])
            day3 = day2.split(',')
            Day = str(day3[0])

            number1 = tostring.split('"number": ')
            number2 = str(number1[1])
            number3 = number2.split(',')
            Number = eval(number3[0])
                
            if Number == 3:
                if Day == 'false':
                    pass
                else:
                    temp1 = tostring.split('"temperature": ')
                    temp2 = str(temp1[1])
                    temp3 = temp2.split(',')
                    Temp = eval(temp3[0])
                    HighList.append(Temp)

                    time1 = tostring.split('"startTime": "')
                    time2 = str(time1[1])
                    time3 = time2.split(':00-05:00",')
                    time4 = str(time3[0])
                    Time = dt.strptime(time4,'%Y-%m-%dT%H:%M')
            if Number == 4:
                if Day == 'false':
                    temp1 = tostring.split('"temperature": ')
                    temp2 = str(temp1[1])
                    temp3 = temp2.split(',')
                    Temp = eval(temp3[0])
                    LowList.append(Temp)
                else:
                    temp1 = tostring.split('"temperature": ')
                    temp2 = str(temp1[1])
                    temp3 = temp2.split(',')
                    Temp = eval(temp3[0])
                    HighList.append(Temp)

                    time1 = tostring.split('"startTime": "')
                    time2 = str(time1[1])
                    time3 = time2.split(':00-05:00",')
                    time4 = str(time3[0])
                    Time = dt.strptime(time4,'%Y-%m-%dT%H:%M')
            if Number == 5:
                if Day == 'false':
                    temp1 = tostring.split('"temperature": ')
                    temp2 = str(temp1[1])
                    temp3 = temp2.split(',')
                    Temp = eval(temp3[0])
                    LowList.append(Temp)
                else:
                    pass
        sections = []

    fig = plt.figure(figsize=(14,7))
    ax = plt.axes()

    ax.set(xlim=(-84.84, -74.85), ylim=(32.0, 36.8))
    plt.xlim(-84.84, -74.85)
    plt.ylim(32.0, 36.8)

    ax.axis('off')

    sf = shp.Reader("NC & SC Counties.shp")

    for shape in sf.shapeRecords():
        for i in range(len(shape.shape.parts)):
            i_start = shape.shape.parts[i]
            if i==len(shape.shape.parts)-1:
                i_end = len(shape.shape.points)
            else:
                i_end = shape.shape.parts[i+1]
            e = [i[0] for i in shape.shape.points[i_start:i_end]]
            f = [i[1] for i in shape.shape.points[i_start:i_end]]
            plt.plot(e,f, color='grey', linewidth=0.3)

    sf = shp.Reader("NC & SC State.shp")

    for shape in sf.shapeRecords():
        for i in range(len(shape.shape.parts)):
            i_start = shape.shape.parts[i]
            if i==len(shape.shape.parts)-1:
                i_end = len(shape.shape.points)
            else:
                i_end = shape.shape.parts[i+1]
            e = [i[0] for i in shape.shape.points[i_start:i_end]]
            f = [i[1] for i in shape.shape.points[i_start:i_end]]
            plt.plot(e,f, color='black', linewidth=0.5)

    font1 = {'fontname':'Candara','size':16,'color':'black','weight':'bold'}
    font2 = {'fontname':'Candara','size':24,'color':'black','weight':'bold'}
    font3 = {'fontname':'Candara','size':24,'color':'goldenrod','weight':'bold'}
    font4 = {'fontname':'Candara','size':24,'color':'royalblue','weight':'bold'}
    font5 = {'fontname':'Candara','size':22,'color':'black','weight':'bold'}
    zcount = 0
    for i,j in zip(Longitude, Latitude):
        plt.text(i-0.17,j-0.14,HighList[zcount],size=16,weight='bold',color='goldenrod',ha='center')
        plt.text(i+0.17,j-0.14,LowList[zcount],size=16,weight='bold',color='royalblue',ha='center')
        plt.text(i,j-0.14,'/',size=16,color='black',ha='center')
        plt.text(i,j+0.08,CityNames[zcount],ha='center',**font1)
        zcount = zcount + 1

    ForecastDay = Time.strftime('%A')
    ForecastDate = Time.strftime('%B %d, %Y')

    im = plt.imread('CWGLogo.png')
    newax = fig.add_axes([0.65, 0.13, 0.2, 0.2], anchor='SE', zorder=-1)
    newax.imshow(im)
    newax.axis('off')

    fig.text(0.5,0.94,'National Weather Service',ha='center',**font2)
    fig.text(0.3,0.88,'High',ha='center',**font3)
    fig.text(0.3375,0.88,'/',ha='center',**font2)
    fig.text(0.37,0.88,'Low',ha='center',**font4)
    fig.text(0.552,0.88,'Temperature Forecast',ha='center',**font2)
    fig.text(0.25,0.22,ForecastDay,ha='center',**font5)
    fig.text(0.25,0.18,ForecastDate,ha='center',**font5)

    plt.savefig('output/NWSForecast2.png',bbox_inches='tight',dpi=300)
    
day2()

def day3():

    stations = open('ForecastPoints.csv')

    sections = []
    HighList = []
    LowList = []
    CityNames = []
    Latitude = []
    Longitude = []

    for line in stations:
        listify = line.split(',')
        x = listify[0]
        y = listify[1]
        city = listify[2]
        CityNames.append(city)
        office = listify[3]
        lat = eval(listify[4])
        Latitude.append(lat)
        lon = eval(listify[5])
        Longitude.append(lon)

        url = 'https://api.weather.gov/gridpoints/{0}/{1},{2}/forecast/'.format(office,x,y)
        html = urllib.request.urlopen(url)
        soup = BeautifulSoup(html,features='html.parser')

        massivestring = str(soup)

        bigsplit = massivestring.split('{')

        count = 0

        for i in bigsplit:
            if count > 5:
                sections.append(i)
            else:
                pass
            count = count + 1

        for i in sections:
            #if limit < 2:
            tostring = str(i)
            day1 = tostring.split('"isDaytime": ')
            day2 = str(day1[1])
            day3 = day2.split(',')
            Day = str(day3[0])

            number1 = tostring.split('"number": ')
            number2 = str(number1[1])
            number3 = number2.split(',')
            Number = eval(number3[0])
                
            if Number == 5:
                if Day == 'false':
                    pass
                else:
                    temp1 = tostring.split('"temperature": ')
                    temp2 = str(temp1[1])
                    temp3 = temp2.split(',')
                    Temp = eval(temp3[0])
                    HighList.append(Temp)

                    time1 = tostring.split('"startTime": "')
                    time2 = str(time1[1])
                    time3 = time2.split(':00-05:00",')
                    time4 = str(time3[0])
                    Time = dt.strptime(time4,'%Y-%m-%dT%H:%M')
            if Number == 6:
                if Day == 'false':
                    temp1 = tostring.split('"temperature": ')
                    temp2 = str(temp1[1])
                    temp3 = temp2.split(',')
                    Temp = eval(temp3[0])
                    LowList.append(Temp)
                else:
                    temp1 = tostring.split('"temperature": ')
                    temp2 = str(temp1[1])
                    temp3 = temp2.split(',')
                    Temp = eval(temp3[0])
                    HighList.append(Temp)

                    time1 = tostring.split('"startTime": "')
                    time2 = str(time1[1])
                    time3 = time2.split(':00-05:00",')
                    time4 = str(time3[0])
                    Time = dt.strptime(time4,'%Y-%m-%dT%H:%M')
            if Number == 7:
                if Day == 'false':
                    temp1 = tostring.split('"temperature": ')
                    temp2 = str(temp1[1])
                    temp3 = temp2.split(',')
                    Temp = eval(temp3[0])
                    LowList.append(Temp)
                else:
                    pass
        sections = []

    fig = plt.figure(figsize=(14,7))
    ax = plt.axes()

    ax.set(xlim=(-84.84, -74.85), ylim=(32.0, 36.8))
    plt.xlim(-84.84, -74.85)
    plt.ylim(32.0, 36.8)

    ax.axis('off')

    sf = shp.Reader("NC & SC Counties.shp")

    for shape in sf.shapeRecords():
        for i in range(len(shape.shape.parts)):
            i_start = shape.shape.parts[i]
            if i==len(shape.shape.parts)-1:
                i_end = len(shape.shape.points)
            else:
                i_end = shape.shape.parts[i+1]
            e = [i[0] for i in shape.shape.points[i_start:i_end]]
            f = [i[1] for i in shape.shape.points[i_start:i_end]]
            plt.plot(e,f, color='grey', linewidth=0.3)

    sf = shp.Reader("NC & SC State.shp")

    for shape in sf.shapeRecords():
        for i in range(len(shape.shape.parts)):
            i_start = shape.shape.parts[i]
            if i==len(shape.shape.parts)-1:
                i_end = len(shape.shape.points)
            else:
                i_end = shape.shape.parts[i+1]
            e = [i[0] for i in shape.shape.points[i_start:i_end]]
            f = [i[1] for i in shape.shape.points[i_start:i_end]]
            plt.plot(e,f, color='black', linewidth=0.5)

    font1 = {'fontname':'Candara','size':16,'color':'black','weight':'bold'}
    font2 = {'fontname':'Candara','size':24,'color':'black','weight':'bold'}
    font3 = {'fontname':'Candara','size':24,'color':'goldenrod','weight':'bold'}
    font4 = {'fontname':'Candara','size':24,'color':'royalblue','weight':'bold'}
    font5 = {'fontname':'Candara','size':22,'color':'black','weight':'bold'}
    zcount = 0
    for i,j in zip(Longitude, Latitude):
        plt.text(i-0.17,j-0.14,HighList[zcount],size=16,weight='bold',color='goldenrod',ha='center')
        plt.text(i+0.17,j-0.14,LowList[zcount],size=16,weight='bold',color='royalblue',ha='center')
        plt.text(i,j-0.14,'/',size=16,color='black',ha='center')
        plt.text(i,j+0.08,CityNames[zcount],ha='center',**font1)
        zcount = zcount + 1

    ForecastDay = Time.strftime('%A')
    ForecastDate = Time.strftime('%B %d, %Y')

    im = plt.imread('CWGLogo.png')
    newax = fig.add_axes([0.65, 0.13, 0.2, 0.2], anchor='SE', zorder=-1)
    newax.imshow(im)
    newax.axis('off')

    fig.text(0.5,0.94,'National Weather Service',ha='center',**font2)
    fig.text(0.3,0.88,'High',ha='center',**font3)
    fig.text(0.3375,0.88,'/',ha='center',**font2)
    fig.text(0.37,0.88,'Low',ha='center',**font4)
    fig.text(0.552,0.88,'Temperature Forecast',ha='center',**font2)
    fig.text(0.25,0.22,ForecastDay,ha='center',**font5)
    fig.text(0.25,0.18,ForecastDate,ha='center',**font5)

    plt.savefig("output/NWSForecast3.png",bbox_inches='tight', dpi=300)
        
day3()
