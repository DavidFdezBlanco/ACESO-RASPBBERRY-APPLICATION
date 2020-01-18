import time
import datetime
import random


millis = int(round(time.time() * 1000))
idline = 1
for line in range(0,3600000):
    if(line % 5000 == 0):
        data = millis - line - 3600000
        date2 = datetime.datetime.fromtimestamp(data/1000.0)
        date = date2.strftime('%Y-%m-%d %H:%M:%S')
        value = 80 - random.randint(0, 10)
        stringPlot = "[Pulse] " + str(value) +",sensor1,"+date+" \n"
        file1 = open("data.txt","a")
        file1.write(stringPlot)
        idline= idline + 1
        
for line in range(0,3600000):
    if(line % 5000 == 0):
        data = millis - line - 3600000
        date2 = datetime.datetime.fromtimestamp(data/1000.0)
        date = date2.strftime('%Y-%m-%d %H:%M:%S')
        value = 37 - random.randint(0, 2)
        stringPlot = "[Temperature] " + str(value) +",sensor2,"+date+" \n"
        file1 = open("data.txt","a")
        file1.write(stringPlot)
