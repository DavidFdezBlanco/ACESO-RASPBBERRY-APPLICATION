import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

############
def genKey(password):
    password_provided = password # This is input in the form of a string
    password = password_provided.encode() # Convert to type bytes
    salt = b'salt_' # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
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
def encryptFile(password, fileName):
	output_file = fileName + ".encrypted"
	key = genKey(password)
	with open(fileName, 'rb') as f:
		data = f.read()
	f = Fernet(key)
	encrypted = f.encrypt(data)
	with open(output_file, 'wb') as f:
		f.write(encrypted)

############
def decryptFile(password, fileName):
	input_file = fileName + ".encrypted"
	key = genKey(password)
	f = Fernet(key)
	with open(input_file, 'rb') as f:
		data = f.read()
	try:
		f = Fernet(key)
		decrypted = f.decrypt(data)
	except InvalidToken:
		print("Wrong password")
		decrypted = ''
	with open("decrypted.txt", 'wb') as f:
		f.write(decrypted)

##### TEST #####
#encryptFile("foo","db.json")
#decryptFile("foo","db.json")
