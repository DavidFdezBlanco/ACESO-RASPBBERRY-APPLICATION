import time, threading
import datetime
import random
import paho.mqtt.client as mqtt #import the client1
import paho.mqtt.publish as publish


def generate_Pulse():
    millis = int(round(time.time() * 1000))
    data = millis - 3600000
    date2 = datetime.datetime.fromtimestamp(data/1000.0)
    date = date2.strftime('%Y-%m-%d %H:%M:%S')
    value = 80 - random.randint(0, 10)
    stringPlot = str(value) +",sensor1"
    publish.single("Pulse", stringPlot, hostname="127.0.0.1", port = 1883)
    threading.Timer(3, generate_Pulse).start()

def generate_Temp():
    millis = int(round(time.time() * 1000))
    data = millis - 3600000
    date2 = datetime.datetime.fromtimestamp(data/1000.0)
    date = date2.strftime('%Y-%m-%d %H:%M:%S')
    value = 37 - random.randint(0, 2)
    stringPlot = str(value) +",sensor2"
    publish.single("Temperature", stringPlot, hostname="127.0.0.1", port = 1883)
    threading.Timer(8, generate_Temp).start()

generate_Pulse()
generate_Temp()


