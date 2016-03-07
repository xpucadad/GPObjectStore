import hashlib

hash_object = hashlib.sha256(b'abc')
hex_dig = hash_object.hexdigest()
print(hex_dig)

buffer = bytearray(3)

buffer[0] = 97
buffer[1] = 98
buffer[2] = 99
print(buffer)

hash_object = hashlib.sha256(buffer)
hex_dig = hash_object.hexdigest()
print(hex_dig)

buffer[0] = 0x61
buffer[1] = 0x62
buffer[2] = 0x63
print(buffer)

hash_object = hashlib.sha256(buffer)
print(hash_object)
print()
hex_dig = hash_object.hexdigest()
print(hex_dig)
folder = hex_dig[0:2]
filename = hex_dig[2:]
print(folder)
print(filename)
print()
n_buffer = buffer[1:]
print(n_buffer)
print()

hash_object = hashlib.sha256()
hash_object.update(b'ab')
hash_object.update(b'\x63')
print(hash_object)
digest = hash_object.digest()
print(digest)
hex_dig = hash_object.hexdigest()
print(hex_dig)
print()

buffer = bytearray()
buffer.extend(b'abc')
print(buffer)
hash_object = hashlib.sha256()
hash_object.update(buffer)
print(hash_object)
hex_dig = hash_object.hexdigest()
print(hex_dig)
