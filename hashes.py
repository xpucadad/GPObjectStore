import hashlib

def sha256x2(data):
    digest = hashlib.sha256(hashlib.sha256(data).digest()).digest()
    return digest

def ripemd160xsha256(data):
    h256_dig = hashlib.new('sha256', data).digest()
    digest = hashlib.new('ripemd160', h256_dig).digest()
    return digest
