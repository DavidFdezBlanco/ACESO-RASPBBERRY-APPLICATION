import paho.mqtt.client as mqtt #import the client1
import paho.mqtt.publish as publish
import time
import datetime
import ttn
import re
import os
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair


filename_REAL_TIME = "receivedFiles/realtime.txt"
REALTIME_file = [None]*1000 #500 dernières traces sur le REALTIME
LARGE_file = [None]*1000
userdId = "Hospital"
bdb_root_url = 'https://test.ipdb.io/'

def sendToBlockchain(input):
    bdb = BigchainDB(bdb_root_url) #init bigchainDb
    user = generate_keypair()

    prepared_creation_tx = bdb.transactions.prepare(
        operation='CREATE',
        signers=user.public_key,
        asset=input
    )
    fulfilled_creation_tx = bdb.transactions.fulfill(
        prepared_creation_tx, private_keys=user.private_key)
    bdb.transactions.send_commit(fulfilled_creation_tx)

    print("Sent to the blockchain")

def isFull():
    for line in REALTIME_file:
        if ((str(None) in str(line)) == True):
            return False
    return True

def writeOutput():
    os.remove(filename_REAL_TIME)
    f = open(filename_REAL_TIME, "a")
    for line in REALTIME_file:
        if ((str(None) in str(line)) == False):
            line= line.replace('\\','')
            f.write(line)
 
def writeLong(longname, list):
    os.remove("receivedFiles/"+longname+"_toTreat.txt")
    f = open("receivedFiles/"+longname+".txt", "a")
    s = ""
    for line in list:
        if ((str(None) in str(line)) == False):
            if (("END" in str(line)) == False):
                line= line.replace('\\','')
                s += str(line)
                f.write(line)
    if(s != ""):
        block = {'data': {'user': userdId,'content':s},}
        sendToBlockchain(block)
            
def cleanRealTime():
    f = open(filename_REAL_TIME, "r")
    for line in f:
        if(isFull() == False):
            #print(line)
            lineNumber = line.split("]")[1]
            lineNumber = lineNumber.replace(";[","")
            #print("line number " + str(lineNumber))
            REALTIME_file[int(lineNumber)] = line
        else:
            print("case not treated jet")
    writeOutput()
    
def cleanLargeFile(name):
    LARGE_file = [None]*5000
    f = open("receivedFiles/"+name+"_toTreat.txt", "r")
    for line in f:
        linesplitted = line.split("]!")[0]
        fragmentNumberField = linesplitted.split("][")
        finalPayload = line.split("]!")[1].replace("\n", "")
        finalPayload = finalPayload.replace("\\n","\n")
        fragmentNumber = int(fragmentNumberField[0].replace("[IDPCK:",""))
        LARGE_file[fragmentNumber] = finalPayload
    writeLong(name,LARGE_file)
    
#def cleanLongFile(filename):

#manque verifier qu'elle n'est pas deja dedans dans realtime
def storeTrace(store):
    Payload = store[6]
    PayloadClean = Payload[0]
    stringSplitted = PayloadClean.split("]!")
    entetes = stringSplitted[0].split("][")
    payload = stringSplitted[1]
    if(("REAL" in str(entetes[0])) == True):
        print("*** REALTIME Message received " + PayloadClean)
        file1 = open(filename_REAL_TIME,"a")
        file1.write(payload)
    elif(("test" in str(entetes[0])) == True):
        print("Sender searching for most optimal channel")
    else:
        print("*** Large Message received " + PayloadClean)
        idPCK = str(entetes[1].replace("]",""))
        filename = "receivedFiles/" + str(entetes[1].replace("]","")) + "_toTreat.txt"
        file1 = open(filename,"a")
        PayloadToAdd = PayloadClean.replace("b'", "")
        PayloadToAdd = PayloadToAdd.replace("'", "")
        file1.write(PayloadToAdd + "\n")
        if(("END" in str(PayloadClean)) == True):
            #print("cleaning")
            cleanRealTime()
            cleanLargeFile(str(idPCK))

#Method on message
def uplink_callback(msg, client):
    #print("Received uplink from ", msg.dev_id)
    storeTrace(msg)
 
 

# Connect to MQTT
broker_address="eu.thethings.network"
usernameTTN = "pils-connect-v1"
passwordTTN = "ttn-account-v2.6kL-TcMRKhqHj0oeXuehRY6sTayZIE6UmjKSA9dfa6Y"
topic = "pils-connect-v1/devices/+/up"



print("--------------------------------------------")
print("Connecting to thethingsnetwork")

handler = ttn.HandlerClient(usernameTTN, passwordTTN)

# using mqtt client
mqtt_client = handler.data()
mqtt_client.set_uplink_callback(uplink_callback)
mqtt_client.connect()

time.sleep(300000)
mqtt_client.close()

print("--------------------------------------------")
