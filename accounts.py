import hashes
import logging
import struct
import time

class Account():
    version = struct.pack('I', 1)

    def __init__(self):
        self.public_key = bytes(32)
        self.private_key = self._generatePrivateKey()

    def generateKeys(self):
        seed = struct.pack('I', int(time.time()))
        self.public_key = hashes.sha256x2(seed)
        self._generatePrivateKey()

    def loadFromPublicKey(self, bytestream):
        pass

    def _generatePrivateKey(self):
        pk = bytearray(32)
        print(len(self.public_key))
        for i in range(0, len(self.public_key)):
            pk[i] = self.public_key[i] ^ 0xFF
        self.private_key = bytes(pk)
        #print('public_key:\t',self.public_key)
        #print('private_key:\t',self.private_key)
        return self.private_key

    def getPublicKey(self):
        return self.public_key

    def getPrivateKey(self):
        return self.private_key

    def getAccount(self):
        pass

    def sign(self, message):
        return bytes(32)

def isValid(pk, message, sig):
    return True
