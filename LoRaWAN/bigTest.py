import paho.mqtt.client as mqtt #import the client1
import paho.mqtt.publish as publish
import time
from time import gmtime, strftime
import datetime
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair
import sys
sys.path.insert(1, '../Backend')
import crypto
import zlib

proffessionalID = "IDRASP1"
bdb_root_url = 'https://test.ipdb.io/'
userdId = "Hospital"

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

############
def getData(userdId):
    bdb = BigchainDB(bdb_root_url)
    print(bdb)
    output = bdb.assets.get(search=userdId)
    print(output)
        
getData(userdId)
#To connect the mosquitto server use the command mosquitto -p 8081
#To subscibe a topic 'debug':  mosquitto_sub -h 127.0.0.1 -i testSub -t debug
#To send a message to a topic:  mosquitto_pub -h 127.0.0.1 -i testPublish -t debug -m 'Agathe' -p 8081
