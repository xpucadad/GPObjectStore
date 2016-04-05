import hashlib

def sha256x2(data):
    hashobj = hashlib.sha256(data)
    d1 = hashobj.digest()
    hashobj = hashlib.sha256(d1)
    digest = hashobj.digest()
    return digest
