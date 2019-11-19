# -*- coding: utf-8 -*-
import hashlib, json

class Chain:
    def __init__(self, index, timestamp, data, previous_hash):
        self.blocks = [self.get_genesis_block()]

    def get_genesis_block(self):
        return block(0, datetime.datetime.utcnow(), 'Genesis', '')

    def add_block(self, data, public_key):
         #declare block
         b = block(len(self.blocks), datetime.datetime.utcnow(), data, public_key, self.blocks[len(self.blocks)-1].hash))
         #verify

         #append it
         self.blocks.append(b)
         #save changes


    def get_chain_size(self): # exclude genesis block
        return len(self.blocks)-1
