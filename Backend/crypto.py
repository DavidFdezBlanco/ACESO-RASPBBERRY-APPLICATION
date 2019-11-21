import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import InvalidToken
############
def genSymKey(password):
    password_provided = password # This is input in the form of a string
    password = password_provided.encode() # Convert to type bytes
    salt = bytes(str(os.urandom(16)),'utf-8') # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password)) # Can only use kdf once
    return key

############
def loadAsymKey(path, pwd): #()'private.pem','pass')
    with open(path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=bytes(pwd,'utf-8'),
            backend=default_backend()
        )
    public_key = private_key.public_key()
    return private_key, public_key

############
def loadSymKey(path):
    with open(path, 'rb') as f:
        key = f.read()

    key = str(key).split("'")[1]
    return key

############
def encryptKey(fileName, keyPath, pwd):
	output_file = fileName + ".cypher"
	_ , public_key = loadKey(keyPath,pwd)
	with open(fileName, 'rb') as f:
		data = f.read()
	cyphertext = public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
	with open(output_file, 'wb') as f:
		f.write(cyphertext)

############
def decryptKey(fileName, keyPath, pwd):
    input_file = fileName + ".cypher"
    private_key , _ = loadKey(keyPath, pwd)
    with open(input_file, 'rb') as f:
        data = f.read()
    decrypted = private_key.decrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    with open("decrypted.txt", 'wb') as f:
        f.write(decrypted)

############
#Attention, data must be in bytes format
def encryptStr(data, keyPath):
    data = bytes(data, 'utf-8')
    symKey = loadSymKey(keyPath)
    f = Fernet(symKey)
    cyphertext = f.encrypt(data)
    return cyphertext

############
def decryptStr(data, keyPath):
    symKey = loadSymKey(keyPath)
    try:
        f = Fernet(symKey)
        decrypted = f.decrypt(data)
    except InvalidToken:
        print("Wrong password")
        decrypted = ''
    return decrypted

##### TESTS #####
#encryptKey("message","keyPath","pass")
#decryptKey("message","keyPath","pass")


#cypher = encryptStr("holita","symKey")
#print(cypher)
#output = decryptStr(cypher,"symKey")
#print(output)
#output = decryptStr(cypher,"symKey2")
#print(output)
