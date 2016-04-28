import hashes
import logging
import random
import struct
import time

class Account():
    version = struct.pack('I', 1)
    public_key_size = 32    # 256 bits
    private_key_size = 32   # 256 bits

    def __init__(self, name):
        self.name = name
        # self.private_key = bytes(32)
        # self.public_key = self._generatePublicKey()
        # self.address = self._generateAddress()

    def generateKeys(self):
        # Create a seed - note that this is not random enough to be really
        # secure. Remember this code is only to show processes, not to
        # provide a secure implementation
        seed = bytearray(struct.pack('d', time.time()))
        seed.extend(struct.pack('d', random.random()))
        logging.debug('generateKeys: seed: %s', seed.hex())
        self.private_key = hashes.sha256x2(seed)
        logging.debug('generateKeys: private key: %s', self.private_key.hex())
        self.__generatePublicKey()
        self.__generateAddress()

    def loadFromPublicKey(self, bytestream):
        pass

    def __generatePublicKey(self):
        self.public_key = self.private_key
        logging.debug('__generatePublicKey: public_key: %s', self.public_key.hex())
        return self.public_key

    def __generateAddress(self):
        self.address = hashes.ripemd160xsha256(self.public_key)
        logging.debug('__generateAddress: address: %s',self.address.hex())
        return self.address

    def getPublicKey(self):
        return self.public_key

    def getPrivateKey(self):
        return self.private_key

    def getAddress(self):
        return self.address

    def getB58Address(self):
        typed_address = bytearray(1)
        typed_address[0] = 0x00 # Type for address
        typed_address.extend(self.address)
        address = hashes.b58encodecheck(typed_address)
        return address

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    # message is expected to be in bytes
    def sign(self, message):
        msg_hash = hashes.sha256x2(message)
        logging.debug('sign: msg_hash: %s', msg_hash.hex())
        signature = bytearray(32)
        for i in range(32):
            signature[i] = msg_hash[i] ^ self.private_key[i]
        logging.debug('sign: signature: %s', signature.hex())
        return bytes(signature)

    def toBytes(self):
        logging.debug('Address.toBytes')
        buffer = bytearray()
        buffer.extend(self.private_key)
        buffer.extend(self.public_key)
#        print('len of address:', len(self.address))
        buffer.extend(self.address)
        name_in_bytes = bytes(self.name, 'utf-8')
#        print('name', name_in_bytes)
#        print('len', len(name_in_bytes))
        buffer.extend(struct.pack('I', len(name_in_bytes)))
        buffer.extend(name_in_bytes)
        return bytes(buffer)

    def fromBytes(self, bytestream):
        logging.debug('Address.fromBytes')
        self.private_key = bytestream[0:32]
        self.public_key = bytestream[32:64]
        self.address = bytestream[64:84]

        name_length = struct.unpack('I', bytestream[84:88])[0]
        name = bytestream[88:88+name_length]
        self.name = name.decode()

    def equals(self, target):
        theSame = (
            self.private_key == target.getPrivateKey()
            and self.public_key == target.getPublicKey()
            and self.address == target.getAddress()
            # and self.name == target.getName() # name can be different
        )
        return theSame

    def __repr__(self):
        if (self.name == ''):
            name = '<unnamed>'
        else:
            name = "\'" + self.name + "\'"

        output = 'Account: ' + name + '\n' + \
            '\tPrivate Key:\t' + self.private_key.hex() + '\n' + \
            '\tPublic Key:\t' + self.public_key.hex() + '\n' + \
            '\tAddress:\t' + self.address.hex() + '\n' + \
            '\tB58 Address:\t' + self.getB58Address()
        return output

    def __str__(self):
        return self.__repr__()

def isValid(pk, message, sig):
    logging.debug('isValid: key: %s',pk.hex())
    logging.debug('isValid: message: %s',message.hex())
    logging.debug('isValid: sig: %s',sig.hex())
    msg_hash = hashes.sha256x2(message)
    msg_hash_from_sig = bytearray(32)
    for i in range(32):
        msg_hash_from_sig[i] = sig[i] ^ pk[i]
    logging.debug('isValid: msg_hash: %s',msg_hash.hex())
    logging.debug('isValid: msg_hash_from_sig: %s', msg_hash_from_sig.hex())
    return (msg_hash == msg_hash_from_sig)
