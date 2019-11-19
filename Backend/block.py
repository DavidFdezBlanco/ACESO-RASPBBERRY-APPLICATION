# -*- coding: utf-8 -*-
import hashlib, json
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
import ecdsa

class Block:
    def __init__(self, timestamp, data, pub_key, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.pub_key = pub_key #patients pub key
        self.previous_hash = previous_hash
        self.hash = self.hashing()
        self.signature = "" #To Do

    def hashing(self):
        key = hashlib.sha256()
        key.update(str(self.index).encode('utf-8'))
        key.update(str(self.timestamp).encode('utf-8'))
        key.update(str(self.data).encode('utf-8'))
        key.update(str(self.pub_key).encode('utf-8'))
        key.update(str(self.previous_hash).encode('utf-8'))
        return key.hexdigest()
