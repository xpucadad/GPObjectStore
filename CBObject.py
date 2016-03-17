import struct
import hashlib
import time

class CBObject():
    # Header Fields
    header = bytearray()
    header_digest = bytearray()
    version = struct.pack("I", 1)
    previous_block_hash = bytearray()
    #merkle_root = bytearray(32)
    content_digest = bytearray()
    time_stamp = bytearray()
    difficulty_target = bytearray(4)
    #nonce = bytearray(4)
    # Data Fields
    content_size = bytearray(4)
    content = bytearray()

    def setData(self, data):
        self.content_size = struct.pack('I', len(data))
        self.content.extend(data)
        self.content_digest = self.sha256x2(self.content)
        self.time_stamp = struct.pack('I', int(time.time()))
        print(self.time_stamp.hex())
        return

    def farm(self, pbh):
        self.previous_block_hash.extend(pbh)

        # create the header bytearray
        self.header.extend(self.version)
        self.header.extend(self.previous_block_hash)
        self.header.extend(self.content_digest)
        self.header.extend(self.time_stamp)
        self.header.extend(self.difficulty_target)
        # nonce starts at 0
        nonce = 0
        self.header.extend(struct.pack('I', nonce))
        loop = 4

        farmed = 0
        while not farmed:
            test_digest = self.sha256x2(self.header)
            # test_digest < generated difficulty_target
            if (nonce > loop):
                self.header_digest = test_digest
                farmed = 1
            else:
                nonce += 1
                self.header[76:80] = struct.pack('I',nonce)

        return self.header_digest

    def sha256x2(self, data):
        hashobj = hashlib.sha256(data)
        d1 = hashobj.digest()
        hashobj = hashlib.sha256(d1)
        digest = hashobj.digest()
        return digest

    def dumpHeader(self):
        print(self.header.hex())

class CBObjectFactory:

    def createNew(self, data):
        block = CBObject()
        block.setData(data)
        return block

    def addToChain(self):
        pass

    def loadFromChain(self, height):
        pass
