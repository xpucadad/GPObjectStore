import hashlib

class Object:
    object_folder = "./objects"

    def __init__(self):
        self.data = bytearray()
        self.hexdigest = ''

    def setData(self,data):
        self.data.extend(data)

    def getHexDigest(self):
        if (self.hexdigest == ''):
            hashobj = hashlib.sha256(self.data)
            self.hexdigest = hashobj.hexdigest()

        return self.hexdigest
