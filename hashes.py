import hashlib
import math

__b58chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
__b58base = len(__b58chars)

# v is a bytes or bytearray
def b58encode(v):
    # convert to a value we can do math on
    long_value = int.from_bytes(v,'big')

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

    # Apparently BitCoin does something to make sure
    # leading zeroes in the byte values are not lost
    #!! This doesn't seem to do anything - nPad always
    # ends up as 0, so nothing is added!
    nPad = 0
    for c in v:
        if c == '\0': nPad += 1
        else: break

    return (__b58chars[0]*nPad) + result

def __sha256(data):
    return hashlib.sha256(data).digest()

def sha256x2(data):
    return __sha256(__sha256(data))

def __ripemd160(data):
    return hashlib.new("ripemd160", data).digest()

def ripemd160xsha256(data):
    return __ripemd160(__sha256(data))
