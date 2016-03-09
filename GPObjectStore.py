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
