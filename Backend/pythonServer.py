# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt #import the client1
import paho.mqtt.publish as publish
from time import gmtime, strftime
import datetime
from tinydb import TinyDB, Query
import crypto
import time, threading


proffessionalID = "IDRASP1"
userdId = "Johnny"
dbMaxSize = 10
bdb_root_url = 'https://test.ipdb.io/'

############
def sendToBlockchain(input):
    bdb = BigchainDB(bdb_root_url) #init bigchainDb
    user = generate_keypair()

    #encrypt the input
    #crypto.encryptFile(password, fileName)

    prepared_creation_tx = bdb.transactions.prepare(
        operation='CREATE',
        signers=user.public_key,
        asset=input
    )
    fulfilled_creation_tx = bdb.transactions.fulfill(
        prepared_creation_tx, private_keys=user.private_key)
    bdb.transactions.send_commit(fulfilled_creation_tx)

    print("A total of " + str(dbMaxSize) + " were sent to the blockchain")

############
def updateTxt():
    db = TinyDB("db.json") #init db
    if(len(db)>dbMaxSize): #if db is too big, send everything to the blockchain
        print("sending" + str(db.all()))
        noow = strftime("%Y-%m-%d %H:%M:%S", gmtime()) #get date
        cypher = crypto.encryptStr(str(db.all()),"symKey") #encrypt data
        block = {'data': {'user': userdId, 'timestamp':str(noow) ,'content':str(cypher)},}
        sendToBlockchain(block) #To query: bdb.assets.get(search='Johnny')
        open('db.json', 'w').close() #resets the local db
    else:
        with open('data.txt', 'w') as f:
            #Just for pulse for the moment
            data = db.search(Query()['topic']=="pulse")
            for key, value, timestamp in data:
                f.write("[" + key + "] " + value + ","+timestamp+"\n")
    threading.Timer(10, updateTxt).start() #Update the txt every 10 seconds

############
def on_message(client, userdata, message):
    received = str(message.payload.decode("utf-8"))
    noow = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print("-----> Message arrived : [" + message.topic + "] " + received + ","+str(noow))
    #IncludeInDB
    sendOtherCompRealTime(client, userdata, "[" + message.topic + "] " + received + ","+str(noow))
    db.insert({'topic': message.topic, 'value': received, 'timestamp': str(noow)})

############
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
client.subscribe("Pulse")

db = TinyDB("db.json") #init db
updateTxt()


time.sleep(10000000000000000) # wait
client.loop_stop() #stop the loop

#To connect the mosquitto server use the command mosquitto -p 8081
#To subscibe a topic 'debug':  mosquitto_sub -h 127.0.0.1 -i testSub -t debug
#To send a message to a topic:  mosquitto_pub -h 127.0.0.1 -i testPublish -t debug -m 'Agathe' -p 8081
