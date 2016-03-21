import hashlib
import struct
import time

from CBObject import CBObject, CBObjectFactory

class CBlockChain():
    filename = ''
    height_list = []
    block_dict = {}
    chain_height = 0

    def loadFromFile(self, filename):
        self.filename = filename
        factory = CBObjectFactory()
        print('filename: ', self.filename)
        with open(self.filename, 'rb') as f:
            done = False
            while not done:
                print('chain_height: ', self.chain_height)
                raw_block_size = f.read(4)
                if len(raw_block_size) == 4:
                    print('raw_block_size: ', raw_block_size)
                    block_size = struct.unpack('I', raw_block_size[0:4])[0]
                    block = bytearray(4 + block_size)
                    block[0:4] = raw_block_size
                    block[4:4+block_size] = f.read(block_size)
                    block_object = factory.loadFromBytes(block)
                    block_header_digest = block_object.header_digest
                    self.block_dict[block_header_digest] = block_object
                    self.height_list.append(block_header_digest)
                else:
                    self.chain_height = len(self.height_list)
                    done = True

        return self.chain_height

    def getBlock(self, block_height):
        block_digest = self.height_list[block_height]
        block = self.block_dict[block_digest]
        return block

    def getBlockContent(self, block_height):
        block = self.getBlock(block_height)
        content = block.getContent()
        return content
        
