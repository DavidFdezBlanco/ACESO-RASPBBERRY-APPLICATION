#!/usr/bin/env python3
"""
    Test harness for dragino module - sends hello world out over LoRaWAN 5 times
"""
import logging
from time import sleep
import RPi.GPIO as GPIO
from libs/dragino import Dragino

max_size = 200  #max bytes size supported by lorawan protocol. 2 bytes from i
min_size = 40  #kinda arbitrary


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

    print("Chunk size is " + str(chunk_size))
    output = []  #The fragmented file
    packetID = 1
    with open(file,'rb') as ifile:
        while True:
            prefix = "[IDPCK:" + str(packetID) + "]!"
            prefix_as_bytes = str.encode(prefix)
            data = ifile.read(chunk_size)
            if data.decode() == "":
                    break
            result = prefix_as_bytes + data
            output.append(result)
            packetID = packetID + 1
        return output

def utf8len(s):
    return len(s.encode('utf-8'))

def getRealSF(s):
    if(s == 3):
        return 12
    if(s == 4):
        return 10
    if(s == 5):
        return 7

def send_file_retransmission_static_size(file, SF): #modify according to protocl
    fragmented_file = fragment(SF, file)
    i = 1
    for block in fragmented_file:
        D.send(str(block))
        print("block " + str(i) + "/" + str(len(fragmented_file)) + " has been sent")
        i+=1
        sleep(1)

def send_file_redondance_static_size(file, numberOfRetrans, SF): #send file
    fragmented_file = fragment(SF, file)
    i = 1
    for block in fragmented_file:
        for x in range(numberOfRetrans):
            D.send(str(block))
            print("retransmission " + str(x) + "/" + str(numberOfRetrans))
            sleep(0.3)
        print("block " + str(i) + "/" + str(len(fragmented_file)) + " has been sent")
        i+=1
    
def send_file_historique_static_size(file, historiqueWindow, SF):
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


#send_file_historique_static_size("large.txt",10)
#send_file(7,"large.txt")

D = Dragino("configs/dragino"+str(7)+".ini", logging_level=logging.WARN)
D.join()
while not D.registered():
    print("Waiting")
    sleep(2)
sleep(2)
optimalIndex = D.send_connection_test("testing connection")
GPIO.cleanup()
sleep(1)
    
SF = getRealSF(optimalIndex)
print("Sarting with SF" + str(SF))
D = Dragino("configs/dragino"+str(SF)+".ini", logging_level=logging.WARN)
D.join()
while not D.registered():
    print("Waiting")
    sleep(2)
sleep(2)

send_file_redondance_static_size("large.txt",3, SF)

