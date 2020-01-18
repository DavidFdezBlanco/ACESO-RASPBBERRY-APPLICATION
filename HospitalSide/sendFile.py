import time, threading
import datetime
import random
import paho.mqtt.client as mqtt #import the client1
import paho.mqtt.publish as publish


def send_file(f):
    file=open(f, "r")
    message = file.read()
    print(message)
    bufferToSend = message
    publish.single("Autoevaluation", bufferToSend, hostname="127.0.0.1", port = 1883)

send_file('filesToSend/Autoeval/autoevaluationData.txt')
