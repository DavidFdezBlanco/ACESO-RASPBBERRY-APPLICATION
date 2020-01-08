#!/usr/bin/env python3
"""
    Test harness for dragino module - sends hello world out over LoRaWAN 5 times
"""
import time
import datetime
import random
import logging
import os
from time import sleep
import RPi.GPIO as GPIO
from libs.dragino import Dragino

max_size = 150  #max bytes size supported by lorawan protocol. 2 bytes from i
min_size = 40  #kinda arbitrary
lastindex = 1
realTimeBatch = [None] * 800

#returns an array of blocks
def fragment(SF, file):
    if(SF < 7 or SF > 12):
        raise Exception("SF should be between 7 and 12")
    if(SF == 7):
        chunk_size = max_size
    elif(SF == 8):
        chunk_size = max_size
    elif(SF == 9):
        chunk_size = 123-30
    elif(SF == 10):
        chunk_size = min_size
    elif(SF == 11):
        chunk_size = min_size
    else:
        chunk_size = min_size

#    print("Chunk size is " + str(chunk_size))
    output = []  #The fragmented file
    packetID = 1
    packetHash = random.randint(1, 10000)
    with open(file,'r') as fileToSave:
        with open("sentFiles/"+str(packetHash)+".txt","w") as fileToWrite:
            dataToSave = fileToSave.read()
            fileToWrite.write(dataToSave)

    with open(file,'rb') as ifile:
        while True:
            prefix = "[IDPCK:" + str(packetID) + "]" + "[" + str(packetHash)  + "]!"
            prefix_as_bytes = str.encode(prefix)
            data = ifile.read(chunk_size)
            if data.decode() == "":
                    result = prefix_as_bytes + str.encode("[END]")
                    output.append(result)
                    break
            result = prefix_as_bytes + data
            output.append(result)
            packetID = packetID + 1
        return output

def utf8len(s):
    return len(s.encode('utf-8'))

def getRealSF(s):
    if(s == 5):
        return 12
    if(s == 4):
        return 10
    if(s == 3):
        return 7

def send_file_retransmission_static_size(D,file, SF): #modify according to protocl
    fragmented_file = fragment(SF, file)
    i = 1
    for block in fragmented_file:
        D.send(str(block))
        print("block " + str(i) + "/" + str(len(fragmented_file)) + " has been sent")
        i+=1
        sleep(1)

def send_file_redondance_static_size(D,file, numberOfRetrans, SF): #send file
    fragmented_file = fragment(SF, file)
    i = 1
    for block in fragmented_file:
        for x in range(numberOfRetrans):
            D.send(str(block))
#            print("retransmission " + str(x) + "/" + str(numberOfRetrans))
            sleep(0.3)
        print("block " + str(i) + "/" + str(len(fragmented_file)) + " has been sent")
        i+=1
    
def send_file_historique_static_size(D, file, historiqueWindow, SF):
    fragmented_file = fragment(SF, file)
    i = 1
    sending = [None]*historiqueWindow
    for block in fragmented_file:
        sending[1:historiqueWindow] = sending[0:historiqueWindow-1]
        sending[0] = block
        for x in range(historiqueWindow):
            if ((str(None) in str(sending[x])) == False):
                D.send(str(sending[x]))
                sleep(0.3)
        print("block " + str(i) + "/" + str(len(fragmented_file)) + " has been sent")
        i+=1
        
GPIO.setwarnings(False)


def consumeRealTimeBatch(D):
    global lastindex
    packetHash = random.randint(1, 10000)
    prefix = "[REALTIME]" + "[" + str(packetHash)  + "]!"
    data = int(round(time.time() * 1000))
    date2 = datetime.datetime.fromtimestamp(data/1000.0)
    date = date2.strftime('%Y-%m-%d %H:%M:%S')
    value = 80 - random.randint(0, 10)
    message = "[Pulse];["+str(lastindex)+"] " + str(value)+ ",sensor1,"+date+"\n" 
    D.send(prefix + message)
    sleep(0.3)
    D.send(prefix + message)
    sleep(0.3)
    D.send(prefix + message)
    sleep(0.3)
    lastindex += 1
    file1 = open("filesToSend/data.txt","a")
    file1.write(message)
    print("***Real time message"+str(lastindex)+" sent")
    
def getOptimalChannelSF():
    D = Dragino("configs/dragino"+str(7)+".ini", logging_level=logging.WARN)
    D.join()
    while not D.registered():
        print("Waiting")
        sleep(2)
    sleep(2)
    optimalIndex = D.send_connection_test("testing connection")
    GPIO.cleanup()
    sleep(1)
    return getRealSF(optimalIndex)

def stablish_session():
    SF = getOptimalChannelSF()
    print("Restarting channel with sf" + str(SF))
    D = Dragino("configs/dragino"+str(SF)+".ini", logging_level=logging.WARN)
    D.join()
    
    while not D.registered():
        print("Waiting")
        sleep(2)
    sleep(2)
    
    numberOfSends = 0
    while numberOfSends < 20:
        numberOfSends += 1
        consumeRealTimeBatch(D)
        if (numberOfSends == 10 or numberOfSends == 20):
            send_file_redondance_static_size(D,"filesToSend/data.txt",4, SF)
            os.remove("filesToSend/data.txt")
    GPIO.cleanup()


while True:
    stablish_session()
