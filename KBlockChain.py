import hashlib
import struct
import time

def main():
    content1 = b"The quick brown fox jumps over the lazy dog."

    # Gather all the salient properties of the data
    data = bytearray(content1)
    data_len = len(data)
    data_digest = sha256x2(data)

    # Create the block header - total 80 bytes
    #   version - 4 bytes: block format version
    #   previous_block_hash - 32 bytes
    #   data_hash (replaces merkle_root) - 32 bytes
    #   time_stamp - 4 bytes
    #   difficulty_target - 4 bytes
    #   nonce - 4 bytes
    header = bytearray()
    version = struct.pack('I', 1)  # version 1
    header.extend(version)
    previous_header_hash = bytearray(32)
    header.extend(previous_header_hash)
    header.extend(data_digest)
    time_stamp = struct.pack('I', int(time.time()))
    header.extend(time_stamp)
    nonce = struct.pack('I', 0)
    header.extend(nonce)
    header = mine_header(header)
    block_length = struct.pack('I', 80 + data_len)

    block = bytearray()
    block.extend(block_length)
    block.extend(header)
    block.extend(struct.pack('I', data_len))
    block.extend(data)

    print(block.hex())

def mine_header(header):
    return header

def sha256x2(stuff):
    hashobj = hashlib.sha256(stuff)
    d1 = hashobj.digest()
    hashobj = hashlib.sha256(d1)
    digest = hashobj.digest()
    return digest

if __name__=="__main__":
   main()
