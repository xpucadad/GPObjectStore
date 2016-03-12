import hashlib
import struct
import time

class Object:
    object_folder = "./objects"
    data = bytearray(0)
    digest = bytearray(0)

    def __init__(self):
        pass

    def extendData(self,stuff):
        self.data.extend(stuff)

    def sha256x2(self):
        if len(self.digest) == 0:
            hashobj = hashlib.sha256(self.data)
            d1 = hashobj.digest()
            hashobj = hashlib.sha256(d1)
            self.digest = hashobj.digest()
        return self.digest

    def print_data(self):
        print(self.data.hex())

    def print_digest(self):
        print(self.digest.hex())

class BTCBlock(Object):
    block_size = bytearray(4)
    block_header = bytearray(80)
    block_content = bytearray()


class BTCBlockHeader(Object):
    version = struct.pack("I", 1)
    previous_block_hash = bytearray(32)
    merkle_root = bytearray(32)
    time_stamp = bytearray(4)
    difficulty_target = bytearray(4)
    nonce = bytearray(4)

    def __init__(self,pbh,dt):
        self.data = bytearray()
        self.previous_block_hash = pbh
        self.difficulty_target = dt
        self.setTimeStamp()

    def setTimeStamp(self,value = 0):
        if (value == 0):
            value = int(time.time())

        self.time_stamp = struct.pack("I", value)

    def hashHeader(self):
        self.extendData(self.version[0:])
        self.extendData(self.previous_block_hash)
        self.extendData(self.merkle_root)
        self.extendData(self.time_stamp)
        self.extendData(self.difficulty_target)
        self.extendData(self.nonce)
        return self.sha256x2()
