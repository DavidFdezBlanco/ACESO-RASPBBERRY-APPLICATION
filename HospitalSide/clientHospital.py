import paho.mqtt.client as mqtt #import the client1
import paho.mqtt.publish as publish
from time import gmtime, strftime
import datetime
from tinydb import TinyDB, Query
import time, threading
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair
import zlib
import os

proffessionalID = "IDRASP1"
userdId = "Johnny"
bdb_root_url = 'https://test.ipdb.io/'
realtimeDataFile = 'receivedFiles/realTime/'+userdId+'.txt'

def on_message(client, userdata, message):
    received = str(message.payload.decode("utf-8"))
    noow = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print("-----> Message arrived : [" + message.topic + "] " + received)
    file = open("receivedFiles/realtime/realtime.txt", "a")
    file.write("[" + message.topic + "] " + received + "\n")

########### MAIN LOOP ############
broker_address="127.0.0.1"
port = 1883
id = "PCAAA"
print("--------------------------------------------")
print("Creating new instance")
client = mqtt.Client("P2") #create new instance
client.on_message=on_message #attach function to callback
print("Connecting to broker")

client.connect(broker_address, port) #connect to broker
client.loop_start() #start the loop

print("Subscribing to topic toServer")
client.subscribe(proffessionalID)

db = TinyDB("db.json") #init db
noow = strftime("%Y-%m-%d %H:%M:%S", gmtime()) #get date

time.sleep(100000) # wait
client.loop_stop() #stop the loop

