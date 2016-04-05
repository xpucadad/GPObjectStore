import hashes
import logging
import struct
import time

class Block():
    # Class variables
    raw_difficulty_target = b'\x20\x03\xa3\x0c'
    hex_difficulty_target = ''
    version = struct.pack("I", 1)

    def __init__(self):
        logging.debug('Block.__init__')
        # Generate the class level diffulty on the 1st instantiation
        if len(Block.hex_difficulty_target) == 0:
            self.generateHexDifficulty()

    # Get the hex string that represents the difficulty target digest
    # This generates a class level variable so it should only be called
    # the first time an object is instantiated from the class.
    def generateHexDifficulty(self):
        logging.debug('Generating the hex difficulty string. Should only happen once per script execution!')
        # Extract the exponent from the difficulty target
        # and convert to an integer
        eraw = bytearray(Block.raw_difficulty_target)
        eraw[1:4] = b'\x00\x00\x00'
        exponent = struct.unpack('I', eraw)[0] - 3

        # Calculate where the mantissa starts in the final dt
        # total length minus mant length minus exponent
        mantstart = 32 - 3 - exponent

        # Create the final difficult target
        dt = bytearray(32)
        dt[mantstart:mantstart+3] = self.raw_difficulty_target[1:4]
        Block.hex_difficulty_target = dt.hex()

    def setContent(self, data):
        logging.debug('Block.setContent')
        self.content_size = struct.pack('I', len(data))
        self.content = data
        self.content_digest = hashes.sha256x2(self.content)
        self.time_stamp = struct.pack('I', int(time.time()))
        return

    def getContent(self):
        logging.debug('Block.getContent')
        return self.content

    def farm(self, pbh):
        logging.debug('Block.farm')
        self.previous_block_hash = pbh

        # create the header bytearray
        self.header = bytearray()
        self.header.extend(Block.version)
        self.header.extend(self.previous_block_hash)
        self.header.extend(self.content_digest)
        self.header.extend(self.time_stamp)
        self.header.extend(self.raw_difficulty_target)

        # nonce starts at 0
        nonce = 0
        self.header.extend(struct.pack('I', nonce))

        farmed = 0
        while not farmed:
            test_digest = hashes.sha256x2(self.header)
            if test_digest.hex() < Block.hex_difficulty_target:
                self.header_digest = test_digest
                farmed = 1
            else:
                nonce += 1
                self.header[76:80] = struct.pack('I',nonce)

        logging.debug('Block farmed with nonce: %s', nonce)

        return self.header_digest

    # Populate this CBObject from its binary representation
    def parseFromBytes(self, bytestream):
        logging.debug('Block.parseFromBytes')
        # The 1st 4 bytes are the size of block starting after
        # the size.
        total_size = struct.unpack('I', bytestream[0:4])[0]

        # The next 80 bytes are the block header
        self.header = bytestream[4:84]

        # Parse the header into its parts
        self.header_digest = hashes.sha256x2(self.header)
        self.version = self.header[0:4]
        self.previous_block_hash = self.header[4:36]
        self.content_digest = self.header[36:68]
        self.time_stamp = self.header[68:72]
        self.difficulty_target = self.header[72:76]
        self.nonce = self.header[76:80]

        # The 4 bytes right after the header are the number
        # of bytes in the content
        self.content_size = bytestream[84:88]

        # Get the content
        cs = struct.unpack('I', self.content_size)[0]
        self.content = bytestream[88:88+cs]

        # Hash the content and compare the hash to the digest
        # from the header.
        ch = hashes.sha256x2(self.content)
        if ch.hex() != self.content_digest.hex():
            logging.error('Incorrect content hash!')

        # Validate the total size of the block.
        if total_size != 80 + 4 + cs:
            logging.error("Incorrect total size!")

        # Return the CBObject that is us.
        return self

    # Produce the binary block from our attributes.
    def toBytes(self):
        logging.debug('Block.toBytes')
        block_array = bytearray(88)
        if len(self.header_digest) > 0:
            i_content_size = struct.unpack('I', self.content_size)[0]
            total_size = 80 + 4 + i_content_size
            block_array[0:4] = struct.pack('I', total_size)
            block_array[4:84] = self.header
            block_array[84:88] = self.content_size
            block_array.extend(self.content)
        return bytes(block_array)

    # Hash the header and return true if it matches our
    # stored digest for the block header.
    def validateHeaderDigest(self):
        logging.debug('Block.validateHeaderDigest')
        newDigest = hashes.sha256x2(self.header)
        return newDigest.hex() == self.header_digest.hex()

    # def sha256x2(self, data):
    #     hashobj = hashlib.sha256(data)
    #     d1 = hashobj.digest()
    #     hashobj = hashlib.sha256(d1)
    #     digest = hashobj.digest()
    #     return digest

#    def dumpHeader(self):
#        print(self.header.hex())

    def getPreviousBlockHash(self):
        return self.previous_block_hash

class BlockFactory:

    def createNew(self, data):
        logging.debug('BlockFactory.createNew')
        block = Block()
        block.setContent(data)
        return block

    def loadFromBytes(self, bytes):
        logging.debug('BlockFactory.loadFromBytes')
        block = Block()
        block.parseFromBytes(bytes)
        return block
