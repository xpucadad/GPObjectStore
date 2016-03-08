import hashlib
import binascii

class Object:
    object_folder = "./objects"

    def __init__(self):
        self.data = bytearray()
        self.digest = bytearray()
        self.hexdigest = ''

    def setData(self,data):
        self.data.extend(data)

    def getDigest(self):
        if len(self.digest) == 0:
            d1 = self.sha256(self.data)
            self.digest = self.sha256(d1)
            #hex = binascii.hexlify(self.digest)
            #self.hexdigest = hex.decode("utf-8")
            self.hexdigest = self.digest.hex()
        return self.digest

    def getHexDigest(self):
        self.getDigest()
        return self.hexdigest

    def sha256(self, input):
        hashobj = hashlib.sha256(input)
        return hashobj.digest()
