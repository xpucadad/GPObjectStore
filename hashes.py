import hashlib
import math

__b58chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
__b58base = len(__b58chars)

__b58types = {  0x00: '1',   # Bitcoin Address
                0x05: '3',  # Pay-to-Script-Hash Address
             }

# v is a bytes or bytearray
def b58encode(v):
    b58type = v[0]
    data = v[1:]

    # convert to a value we can do math on
    long_value = int.from_bytes(data,'big')

    result = ''
    while long_value >= __b58base:
        # dividing by mod 58 - the remainder
        # represents the next b58it.
        div, remainder = divmod(long_value, __b58base)

        # Prepend the character than reprents the remainder
        result = __b58chars[remainder] + result

        # prep the next iteration
        long_value = div

    # Here long_value is the most significant b58it
    result = __b58chars[long_value] + result

    type = __b58types[b58type]

    return type + result

def __sha256(data):
    return hashlib.sha256(data).digest()

def sha256x2(data):
    return __sha256(__sha256(data))

def __ripemd160(data):
    return hashlib.new("ripemd160", data).digest()

def ripemd160xsha256(data):
    return __ripemd160(__sha256(data))
