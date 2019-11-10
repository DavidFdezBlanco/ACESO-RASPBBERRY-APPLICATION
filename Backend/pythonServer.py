# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt #import the client1
import paho.mqtt.publish as publish
import time
from time import gmtime, strftime
import datetime

proffessionalID = "IDRASP1"

############
def on_message(client, userdata, message):
    received = str(message.payload.decode("utf-8"))
    noow = strftime("%Y-%m-%d_%H:%M:%S", gmtime())
    print("-----> Message arrived : [" + message.topic + "] " + received + ","+str(noow))
    #IncludeInDB 
    sendOtherCompRealTime(client, userdata, "[" + message.topic + "] " + received + ","+str(noow))
    file1 = open("data.txt","a")
    file1.write("[" + message.topic + "] " + received + ","+str(noow)+"\n")
    file1.close()

##########
def sendOtherCompRealTime(client,userdata,message):
    bufferToSend = message
    publish.single(proffessionalID, bufferToSend, hostname="192.168.43.225", port = 8081)
    
########################################
broker_address="192.168.43.225"
port = 8081
id = "PCAAA"

print("--------------------------------------------")
print("Creating new instance")
client = mqtt.Client("P1") #create new instance
client.on_message=on_message #attach function to callback
print("Connecting to broker")
client.connect("192.168.43.225", 8081) #connect to broker
client.loop_start() #start the loop

print("Subscribing to topic toServer")
client.subscribe("pulse")



time.sleep(10000000000000000) # wait
client.loop_stop() #stop the loop

#To connect the mosquitto server use the command mosquitto -p 8081
#To subscibe a topic 'debug':  mosquitto_sub -h 127.0.0.1 -i testSub -t debug
#To send a message to a topic:  mosquitto_pub -h 127.0.0.1 -i testPublish -t debug -m 'Agathe' -p 8081

