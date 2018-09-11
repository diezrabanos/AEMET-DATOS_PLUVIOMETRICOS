# encoding: utf-8
"""
    The api gives data but not coordinates. I couldn't mine them dinamicaly, aemet provide this data, but
    I needed to copy the html code to 36 files -they just show you items in groups of 30-.
    I include the files and the method, but for further asks, I have passed all the stations with pluviometric
    data to a sqlite3 database, once I knew the stations with pluviometric data after running the script.

    I have also added a variable firstyear. you can set it to 2018 if you want to update the data etc...

    So init method gets data from that database:
    -name of the station
    -code of the station
    -latitude
    -longitude
    -first year available
    -last year available

    Then the resulting array is passed as parameter to the generateJSON method and controls the flux of the monthly urls asked 
    to the api.

    This is an example url if you wish to be certain data are correctly taken from the api.You can change just
    the date (remember the maximum the api shows is 31 days on a single json) and the code of the station (before /?)
    example:
    https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/2018-08-01T00:00:00UTC/fechafin/2018-08-04T23:59:59UTC/estacion/1387E/?api_key=[ENTER YOUR API]
"""
import glob
from bs4 import BeautifulSoup
import os
import urllib2
import json
import time
import sqlite3

class DataMeteorologySpain():
    """You can relaunch it from 2018 next month to fill data
    of the last year -it would override 2018.json file with all
    available 2018 data """
    firstyear = 1812
    """change for your path"""
    path = '/home/manu/Escritorio/AEMET/'
    def __init__(self):
        """timesleep is setted to 60 seconds when every exception happens (there is a check each 50 petitions,
        I tried 30s and 45s and crashes)"""
        finalStations = self.giveMeStations()
        """you can relaunch it from the next station to 160 changing the range -eg range(67,160)"""
        for io in range (0,160):
            print ('Station: ' + str(io+1) + '/160')
            self.generateJSON(finalStations[io])
    """The units of the json keys are at metadata.txt file"""
    def generateJSON(self,arrayDataStations):
        path = 'https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/'
        api = 'api_key='+'ENTER HERE THE API'
        station = arrayDataStations[0]
        stationName = arrayDataStations[1]
        latitude = arrayDataStations[2]
        longitude = arrayDataStations[3]
        ancientYear = int(arrayDataStations[4])
        lastYear = int(arrayDataStations[5])
        print (str(ancientYear) + '/' + str(lastYear))
        if ancientYear<self.firstyear:
            ancientYear=self.firstyear
        for year in range (ancientYear,lastYear+1):
            print(year)
            arrayDictsStation = []
            for month in range (12):
                variablepath = ''
                if month==0 and year>=self.firstyear:
                    variablepath = '-01-01T00:00:00UTC/fechafin/'+str(year)+'-01-31T23:59:59UTC/estacion/'
                elif month==1 and year>=self.firstyear:
                    if year%4==0:
                        variablepath = '-02-01T00:00:00UTC/fechafin/'+str(year)+'-02-29T23:59:59UTC/estacion/'
                    else:
                        variablepath = '-02-01T00:00:00UTC/fechafin/'+str(year)+'-02-28T23:59:59UTC/estacion/'
                elif month==2 and year>=self.firstyear:
                    variablepath = '-03-01T00:00:00UTC/fechafin/'+str(year)+'-03-31T23:59:59UTC/estacion/'
                elif month==3 and year>=self.firstyear:
                    variablepath = '-04-01T00:00:00UTC/fechafin/'+str(year)+'-04-30T23:59:59UTC/estacion/'
                elif month==4 and year>=self.firstyear:
                    variablepath = '-05-01T00:00:00UTC/fechafin/'+str(year)+'-05-31T23:59:59UTC/estacion/'
                elif month==5 and year>=self.firstyear:
                    variablepath = '-06-01T00:00:00UTC/fechafin/'+str(year)+'-06-30T23:59:59UTC/estacion/'
                elif month==6 and year>=self.firstyear:
                    variablepath = '-07-01T00:00:00UTC/fechafin/'+str(year)+'-07-31T23:59:59UTC/estacion/'
                elif month==7 and year>=self.firstyear:
                    variablepath = '-08-01T00:00:00UTC/fechafin/'+str(year)+'-08-31T23:59:59UTC/estacion/'
                elif month==8 and year>=self.firstyear:
                    variablepath = '-09-01T00:00:00UTC/fechafin/'+str(year)+'-09-30T23:59:59UTC/estacion/'
                elif month==9 and year>=self.firstyear:
                    variablepath = '-10-01T00:00:00UTC/fechafin/'+str(year)+'-10-31T23:59:59UTC/estacion/'
                elif month==10 and year>=self.firstyear:
                    variablepath = '-11-01T00:00:00UTC/fechafin/'+str(year)+'-11-30T23:59:59UTC/estacion/'
                elif month==11 and year>=self.firstyear:
                    variablepath = '-12-01T00:00:00UTC/fechafin/'+str(year)+'-12-31T23:59:59UTC/estacion/'
                variable = station + '/?'
                url = path+str(year)+variablepath+variable+api
                print (url)
                try:
                    for line in urllib2.urlopen(url):
                        if 'datos' in line and 'metadatos' not in line and 'satisfagan' not in line:
                            urlData = line[13:-3]
                            try:
                                response = urllib2.urlopen(urlData)
                                data = response.read().decode("latin-1")
                                for jsonday in json.loads(data):
                                    jsonday['latitude'] = latitude
                                    jsonday['longitude'] = longitude
                                    jsonday = self.changeKeys(jsonday)
                                    arrayDictsStation.append(jsonday)
                            except Exception as e:
                                print(e)
                                print ('60s')
                                time.sleep(60)
                                """The code is repeated at both exception candidates in order to fill
                                that month too."""
                                try:
                                    response = urllib2.urlopen(urlData)
                                    data = response.read().decode("latin-1")
                                    for jsonday in json.loads(data):
                                        jsonday['latitude'] = latitude
                                        jsonday['longitude'] = longitude
                                        jsonday = self.changeKeys(jsonday)
                                        arrayDictsStation.append(jsonday)
                                except Exception as e:
                                    print(e)
                                    print ('60s')
                                    time.sleep(60)
                                    """The code is repeated at both exception candidates in order to fill
                                    that month too."""
                                    response = urllib2.urlopen(urlData)
                                    data = response.read().decode("latin-1")
                                    for jsonday in json.loads(data):
                                        jsonday['latitude'] = latitude
                                        jsonday['longitude'] = longitude
                                        jsonday = self.changeKeys(jsonday)
                                        arrayDictsStation.append(jsonday)
                                    pass
                except Exception as e:
                    print(e)
                    print ('60s')
                    time.sleep(60)

                    for line in urllib2.urlopen(url):
                        if 'datos' in line and 'metadatos' not in line and 'satisfagan' not in line:
                            try:
                                urlData = line[13:-3]
                                response = urllib2.urlopen(urlData)
                                data = response.read().decode("latin-1")
                                for jsonday in json.loads(data):
                                    jsonday['latitude'] = latitude
                                    jsonday['longitude'] = longitude
                                    jsonday = self.changeKeys(jsonday)
                                    arrayDictsStation.append(jsonday)
                            except Exception as e:
                                print(e)
                                print ('60s')
                                time.sleep(60)
                                urlData = line[13:-3]
                                response = urllib2.urlopen(urlData)
                                data = response.read().decode("latin-1")
                                for jsonday in json.loads(data):
                                    jsonday['latitude'] = latitude
                                    jsonday['longitude'] = longitude
                                    jsonday = self.changeKeys(jsonday)
                                    arrayDictsStation.append(jsonday)

                                pass
            mypath = 'JSON_STATIONS/'+station.upper()+'_'+stationName.upper().replace('/','-')+'/'
            if not os.path.isdir(mypath):
                os.makedirs(mypath)
            with open(mypath + str(year)+".json","w") as fp:
                json.dump(arrayDictsStation, fp)
    """takes the data of the 160 pluviometric stations
    from the database"""
    def giveMeStations(self):
        conn = sqlite3.connect(self.path+'stations.db')
        c = conn.cursor()
        c.execute("SELECT * FROM PLUVSTATIONS")
        conn.commit()
        finalStations = c.fetchall()
        conn.close()
        return finalStations
    """changes the keys to english and fill with null values
    some of them -not all the stations have all those keys"""
    def changeKeys(self,jsonday):
        if 'racha' in jsonday:
            jsonday['gust'] = jsonday.pop('racha')
        else:
            jsonday['gust'] = None
        if 'sol' in jsonday:
            jsonday['sun'] = jsonday.pop('sol')
        else:
            jsonday['sun'] = None
        if 'horatmin' in jsonday:
            jsonday['hourtmin'] = jsonday.pop('horatmin')
        else:
            jsonday['hourtmin'] = None
        if 'provincia' in jsonday:
            jsonday['province'] = jsonday.pop('provincia')
        else:
            jsonday['province'] = None
        if 'fecha' in jsonday:
            jsonday['date'] = jsonday.pop('fecha')
        else:
            jsonday['date'] = None
        if 'horaPresMax' in jsonday:
            jsonday['hourpresmax'] = jsonday.pop('horaPresMax')
        else:
            jsonday['hourpresmax'] = None
        if 'nombre' in jsonday:
            jsonday['name'] = jsonday.pop('nombre')
        else:
            jsonday['name'] = None
        if 'horaPresMin' in jsonday:
            jsonday['hourpresmin'] = jsonday.pop('horaPresMin')
        else:
            jsonday['hourpresmin'] = None
        if 'horaracha' in jsonday:
            jsonday['hourgust'] = jsonday.pop('horaracha')
        else:
            jsonday['hourgust'] = None
        if 'velmedia' in jsonday:
            jsonday['avgspeed'] = jsonday.pop('velmedia')
        else:
            jsonday['avgspeed'] = None
        if 'indicativo' in jsonday:
            jsonday['code'] = jsonday.pop('indicativo')
        else:
            jsonday['code'] = None
        if 'presMax' in jsonday:
            jsonday['presmax'] = jsonday.pop('presMax')
        else:
            jsonday['presmax'] = None
        if 'presMin' in jsonday:
            jsonday['presmin'] = jsonday.pop('presMin')
        else:
            jsonday['presmin'] = None
        if 'horatmax' in jsonday:
            jsonday['hourtmax'] = jsonday.pop('horatmax')
        else:
            jsonday['hourtmax'] = None
        if 'altitud' in jsonday:
            jsonday['altitude'] = jsonday.pop('altitud')
        else:
            jsonday['altitude'] = None
        return jsonday


if __name__=='__main__':
    DataMeteorologySpain()
