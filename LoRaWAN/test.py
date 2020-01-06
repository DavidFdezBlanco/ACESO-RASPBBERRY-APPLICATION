#!/usr/bin/env python3
"""
    Test harness for dragino module - sends hello world out over LoRaWAN 5 times
"""
import logging
from time import sleep
#import RPi.GPIO as GPIO
#from dragino import Dragino

max_size = 243 - 2  #max bytes size supported by lorawan protocol. 2 bytes from i
min_size = 10  #kinda arbitrary


#returns an array of blocks
def fragment(SF, file):
    if(SF < 7 or SF > 12):
        raise Exception("SF should be between 7 and 12")
    if(SF == 7):
        chunk_size = max_size
    elif(SF == 8):
        chunk_size = min_size + int((max_size-min_size)/5) * 4
    elif(SF == 9):
        chunk_size = min_size + int((max_size-min_size)/5) * 3
    elif(SF == 10):
        chunk_size = min_size + int((max_size-min_size)/5) * 2
    elif(SF == 11):
        chunk_size = min_size + int((max_size-min_size)/5) * 1
    else:
        chunk_size = min_size

    print("Chunk size is " + str(chunk_size))
    output = []  #The fragmented file
    with open(file,'rb') as ifile:
        while True:
            data = ifile.read(chunk_size)
            if data.decode() == "":
                    break
            output.append(data)
        return output

def send_file(SF, file): #modify according to protocl
    fragmented_file = fragment(SF, file)
    i = 1
    for block in fragmented_file:
        D.send(block)
        print("block " + str(i) + "/" + str(len(fragmented_file)) + " has been sent")
        i+=1



GPIO.setwarnings(False)

D = Dragino("dragino.ini", logging_level=logging.DEBUG)
D.join()
while not D.registered():
    print("Waiting")
    sleep(2)
#sleep(10)

#send_file(7,"large.txt")

for i in range(0, 5):
    D.send("Hello World")
    print("Sent message")
    sleep(1)
