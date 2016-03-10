import hashlib

class Object:
    object_folder = "./objects"

    def __init__(self):
        self.data = bytearray()
        self.digest = bytearray()

    def setData(self,data):
        self.data.extend(data)

    def sha256x2(self):
        if len(self.digest) == 0:
            hashobj = hashlib.sha256(self.data)
            d1 = hashobj.digest()
            hashobj = hashlib.sha256(d1)
            self.digest = hashobj.digest()
        return self.digest

class BTCBlock(Object):
    block_size = bytearray(4)
    block_header = bytearray(80)
    block_content = bytearray()


class BTCBlockHeader(Object)
    version = bytearray(0x00000001)
    previous_block_hash = bytearray(32)
    merkle_root = bytearray(32)
    time_stamp = 0
    difficulty_target = bytearray(4)
    nonce = bytearray(4)

    def __init__(self,pbh,dt):
        self.previous_block_hash = pbh
        self.difficulty_target = dt
        self.timestamp = pack("I", int(time.time()))

    def hashHeader(self)
        self.data[0:4] = version[0:]
        self.data[4:36] = self.previous_block_hash
        self.data[36:68] = self.merkle_root
        self.data[68:72] = self.time_stamp
        self.data[72:76] = self.difficulty_target
        self.data[76:80] = self.nonce

        return self.sha256x2()
        
