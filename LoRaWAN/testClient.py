import time
import ttn

app_id = "pils-connect-v1"
access_key = "ttn-account-v2.6kL-TcMRKhqHj0oeXuehRY6sTayZIE6UmjKSA9dfa6Y"

def uplink_callback(msg, client):
  print("Received uplink from ", msg.dev_id)
  print(msg)



# using application manager client
app_client =  handler.application()
my_app = app_client.get()
print(my_app)
my_devices = app_client.devices()
print(my_devices)
