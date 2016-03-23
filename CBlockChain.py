import hashlib
import struct
import time

from CBObject import CBObject, CBObjectFactory

class CBlockChain():
    def __init__(self):
        self.filename = ''
        self.height_list = []
        self.block_dict = {}
        self.chain_height = 0

    def loadFromFile(self, filename):
        self.filename = filename
        factory = CBObjectFactory()
        with open(self.filename, 'rb') as f:
            while True:
                raw_block_size = f.read(4)
                if len(raw_block_size) < 4: break
                block_size = struct.unpack('I', raw_block_size[0:4])[0]
                block = bytearray(4 + block_size)
                block[0:4] = raw_block_size
                block[4:4+block_size] = f.read(block_size)
                block_object = factory.loadFromBytes(bytes(block))
                self.addBlock(block_object)

        return self.chain_height

    def saveToFile(self, filename):
        self.filename = filename

        with open(self.filename, 'wb') as f:
            for i in range(0, self.chain_height):
                header_digest = self.height_list[i]
                block = self.block_dict[header_digest]
                buffer = block.toBytes()
                f.write(buffer)

        return self.chain_height

    def addBlock(self, block):
        header_digest = bytes(block.header_digest)
        self.block_dict[header_digest] = block
        self.height_list.append(header_digest)
        self.chain_height = len(self.height_list)
        return self.chain_height

    def getBlockAtHeight(self, block_height):
        block_digest = self.height_list[block_height]
        block = self.block_dict[block_digest]
        return block

    def getBlockWithDigest(self, block_digest):
        block = self.block_dict[block_digest]
        return block

    def getBlockContent(self, block_height):
        block = self.getBlockAtHeight(block_height)
        content = block.getContent()
        return content

    def getLastBlockDigest(self):
        if len(self.height_list) == 0:
            last_digest = bytes(32)
        else:
            last_digest = self.height_list[-1]
        return last_digest
