import paho.mqtt.client as mqtt #import the client1
import paho.mqtt.publish as publish
import time
import datetime

filename_REAL_TIME = "receivedFiles/realtime.txt"

#manque verifier qu'elle n'est pas deja dedans dans realtime
def storeTrace(str):
    stringSplitted = str.split("]!")
    entetes = stringSplitted[0].split("][")
    payload = stringSplitted[1]
    if(("REALTIME" in str(entetes[0])) == False):
        file1 = open(filename_REAL_TIME,"a")
        file1.write(payload)
    else:
        filename = str(entetes[1].replace("]","")) + "_toTreat.txt"
        file1 = open(filename_REAL_TIME,"a")
        file1.write(payload)
        
def writeOutput(transmission):
    f = open("output.txt", "a")
    for line in transmission:
        if ((str(None) in str(line)) == False):
            line= line.replace('\\','')
            print(line)
            f.write(line)

#Method on message
def on_message(client, userdata, message):
    received = str(message.payload.decode("utf-8"))
    noow = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print("-----> Message arrived : " +  received)
    

# Connect to MQTT
broker_address="eu.thethings.network"
usernameTTN = "pils-connect-v1"
passwordTTN = "ttn-account-v2.6kL-TcMRKhqHj0oeXuehRY6sTayZIE6UmjKSA9dfa6Y"
topic = "pils-connect-v1/devices/+/up"


print("--------------------------------------------")
print("Connecting to thethingsnetwork")
client = mqtt.Client("Client1")
client.username_pw_set(username=usernameTTN,password=passwordTTN)
client.on_message=on_message
client.subscribe(topic)
client.connect(broker_address)
print("--------------------------------------------")

client.loop_start() #start the loop

time.sleep(100000) # wait
client.loop_stop() #stop the loop

