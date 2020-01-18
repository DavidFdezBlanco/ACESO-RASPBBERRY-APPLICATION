import paho.mqtt.client as mqtt #import the client1
import paho.mqtt.publish as publish
from time import gmtime, strftime
import datetime
from tinydb import TinyDB, Query
import crypto
import time, threading
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair
import zlib
import os

proffessionalID = "IDRASP1"
userdId = "Johnny"
dbMaxSize = 10
bdb_root_url = 'https://test.ipdb.io/'

############ METHOD THAT SENDS AN STRING TO THE BLOCKCHAIN
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

############ updates the txt file that shows the data
def updateTxt(noow):
    db = TinyDB("db.json") #init db
    if(len(db)>dbMaxSize): #if db is too big, send everything to the blockchain
        print("sending" + str(db.all()))
        noow = strftime("%Y-%m-%d %H:%M:%S", gmtime()) #get date

        #Encryption
        cypher = crypto.encryptStr(str(db.all()),"symKey") #encrypt data

        #Compression
        compressed_file = zlib.compress(cypher,4)

        #Create final block
        block = {'data': {'user': userdId, 'timestamp':str(noow) ,'content':str(compressed_file)},}
        sendToBlockchain(block) #To query: bdb.assets.get(search='Johnny')
        open('db.json', 'w').close() #resets the local db
    else:
        with open('data.txt', 'a+') as f:
            #Just for pulse for the moment
            data = db.search(Query()['topic']=="Pulse")
            for line in data:
               if(line['timestamp']>noow):
                   f.write("[" + line['topic'] + "] " + line['value'] + ","+line['timestamp']+"\n")
            data = db.search(Query()['topic']=="Temperature")
            for line in data:
               if(line['timestamp']>noow):
                   f.write("[" + line['topic'] + "] " + line['value'] + ","+line['timestamp']+"\n")
                   
    noow = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    threading.Timer(5, updateTxt, [noow]).start() #Update the txt every 5 seconds
    threading.Timer(5, send_autoeval_result).start()

def store_autoeval(data):
    filename = 'receivedFiles/Autoeval/autoevaluationData.txt'
    file=open(filename, "w")
    file.write(data)
    print("Autoevaluation questionary received")
    
def send_autoeval_result():
    path = 'filesToSend/Autoeval/'
    #print(os.walk(path))
    files = []
    for r, d, f in os.walk(path):
        for file in f:
            if '.txt' in file:
                files.append(os.path.join(r, file))
    
    for f in files:
        print(f)
        send_file(f,"autoeval")

def send_file(f,tag):
    file=open(f, "r")
    message = "["+tag+"]" + file.read()
#   print(message)
    bufferToSend = message
    publish.single(proffessionalID, bufferToSend, hostname="127.0.0.1", port = 1883)
    os.remove(f)
    
    
############ Asynchronous call
def on_message(client, userdata, message):
    if(message.topic == "Autoevaluation"):
        received = str(message.payload.decode("utf-8"))
        store_autoeval(received)
    elif(message.topic == "Diagnostiques"):
        print("diag received") #part to be done
    else:
        received = str(message.payload.decode("utf-8"))
        noow = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        print("-----> Message arrived : [" + message.topic + "] " + received + ","+str(noow))
        #IncludeInDB
        sendOtherCompRealTime(client, userdata, "[" + message.topic + "] " + received + ","+str(noow))
        db.insert({'topic': message.topic, 'value': received, 'timestamp': str(noow)})

############
def sendOtherCompRealTime(client,userdata,message):
    bufferToSend = message
    publish.single(proffessionalID, bufferToSend, hostname="127.0.0.1", port = 1883)


########### MAIN LOOP ############
broker_address="127.0.0.1"
port = 1883
id = "PCAAA"
print("--------------------------------------------")
print("Creating new instance")
client = mqtt.Client("P1") #create new instance
client.on_message=on_message #attach function to callback
print("Connecting to broker")

client.connect(broker_address, port) #connect to broker
client.loop_start() #start the loop

print("Subscribing to topic toServer")
client.subscribe("Pulse")
client.subscribe("Temperature")
client.subscribe("Autoevaluation")
client.subscribe("Diagnostiques")

db = TinyDB("db.json") #init db
noow = strftime("%Y-%m-%d %H:%M:%S", gmtime()) #get date
updateTxt(noow)

time.sleep(100000) # wait
client.loop_stop() #stop the loop

#/usr/local/sbin/mosquitto -c /usr/local/etc/mosquitto/mosquitto.conf with brew
#mosquitto_pub -h 127.0.0.1 -i testPublish -t Diagnostiques -m 'texttosend' -p 1883
#mosquitto_pub -h 127.0.0.1 -i testPublish -t Autoevaluation -m 'texttosend' -p 1883
