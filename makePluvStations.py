import glob
from bs4 import BeautifulSoup
import os
import sqlite3
import json

class DataPluvStationsSpain():
    path = '/home/manu/Escritorio/AEMET/'
    keys = []
    def __init__(self):
        """This is a file I used to generate the database and to get all the json keys, 
        but it is no needed to get the data once I provide the database with coordinates"""
        self.giveMeKeys()
    def giveMeKeys(self):
        count = 0
        for f in sorted(glob.glob(self.path+"JSON_STATIONS/**/*.json")):
            with open(f, "r") as file:
                data = json.load(file)
                if len(data)>1:
                    for key in data[0].items():
                        self.keys.append(key[0])
                        count = count + 1
        print (list(set(self.keys)))
        print (count)

    def giveMeTrueStations(self):
        namePluviometricStations = []
        root, dirs, files = os.walk(self.path+"JSON_STATIONS_COPY/").next()
        for directory in dirs:
            posLimit = directory.index('_')
            nameStation = directory[0:posLimit]
            namePluviometricStations.append(nameStation)
        return (namePluviometricStations)
    def giveCoordinatesStations(self):
        multiarrayDataStations = []
        for f in sorted(glob.glob(self.path+"FILES_COORDINATES_STATIONS/*.html")):
            with open(f, "r") as file:
                soup = BeautifulSoup(file, 'html')
                allStationsFields = soup.find_all(attrs={'class':'borde_rb'})
                allStationsIdx = soup.find_all(attrs={'class':'borde_rlb_th'})
                numStations = int(len(allStationsFields)/13)
                for hj in range (numStations):
                    arrayStation = []
                    arrayDataStation = []
                    arrayStation=allStationsFields[hj*13:hj*13+12]
                    arrayDataStation.append(allStationsIdx[hj].getText())
                    arrayDataStation.append(arrayStation[0].getText())
                    arrayDataStation.append(arrayStation[1].getText())
                    arrayDataStation.append(arrayStation[2].getText())
                    arrayDataStation.append(arrayStation[4].getText())
                    arrayDataStation.append(arrayStation[5].getText())
                    multiarrayDataStations.append(arrayDataStation)
        return multiarrayDataStations

if __name__=='__main__':
    DataPluvStationsSpain()
