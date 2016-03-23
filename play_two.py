import hashlib
import struct
import time

hashobj = hashlib.sha256(b'abc')
d1 = hashobj.digest()
hashobj = hashlib.sha256(d1)
digest = hashobj.digest()
print(digest)
hexdigest = digest.hex()
print(hexdigest)

#format = '@16P'
#buffer = struct.pack(format, (digest[i] for i=0 to 15))
#d2 = struct.unpack(format, buffer)

buffer = bytearray(34)
buffer[0] = 0xff
buffer[1] = 0xff
buffer[2:] = digest[0:]
print(buffer.hex())
buf2 = buffer[2:]
print(buf2.hex())

timestamp = int(time.time())
print(timestamp)
bats = struct.pack("I", timestamp)
print(bats, bats.hex())
uts = struct.unpack("I", bats)[0]
print(uts)
