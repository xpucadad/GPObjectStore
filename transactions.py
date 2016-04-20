import hashes
import logging
import struct

class Transaction():
    version = struct.pack('I', 1)

    def __init__(self):
        logging.debug('Transaction.__init__')

    def setContent(self, data):
        logging.debug('Transaction.setContent')
        self.content_size = len(data)
        self.content = data
        self.content_digest = hashes.sha256x2(self.content)
        return

    def getContent(self):
        logging.debug('Transaction.getContent')
        return self.content

    def getDigest(self):
        return self.content_digest

    def parseFromBytes(self, bytestream):
        logging.debug('Transaction.parseFromBytes')

        # Parse off the version
        self.version = bytestream[0:4]

        # Next 4 bytes are the size of the content starting after the
        # size.
        self.content_size = struct.unpack('I', bytestream[4:8])[0]

        # The next total_size bytes are the content.
        self.content = bytestream[8:8+self.content_size]

        return self

    def toBytes(self):
        logging.debug('Transaction.toBytes')
        working = bytearray(8)
        # Move the version as is
        working[0:4] = self.version

        # Now pack the content size
        working[4:8]= struct.pack('I', self.content_size)

        # And now the content itself
        working.extend(self.content)

        logging.debug('Results: %s', working.hex())
        return bytes(working)
