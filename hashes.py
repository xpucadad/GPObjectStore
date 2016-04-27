import hashlib
import logging
import math

__b58chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
__b58base = len(__b58chars)

__b58BtoT = {  0x00: '1',   # Bitcoin Address
                0x05: '3',  # Pay-to-Script-Hash Address
             }

__b58TtoB = {   '1': 0x00,
                '3': 0x05
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

    # Get the type and prepend it to the b58 string.
    type = __b58BtoT[b58type]

    return type + result

def b58decode(v):
    # Strip off the type indicator
    type = v[0]
    data = v[1:]

    # Convert the b58 to a decimal long
    long_value = 0
    for i in range(len(data)):
        long_value = (long_value * __b58base) + __b58chars.find(data[i])

    # Convert the long integer value to a bytearray
    result = bytearray(0)
    while long_value >= 256:
        div, remainder = divmod(long_value, 256)
        result.append(remainder)
        long_value = div
    result.append(long_value)
    # The byte array created is in the wrong order, so reverse it.
    result.reverse()

    # Now return the result with the appropriate type indicator prepended
    return __b58TtoB[type].to_bytes(1,'big') + result

def b58encodecheck(v):
    # We assume the first byte of v is the "version" or type we
    # are encoding
    data = bytearray(v)

    # Generate the check sum, and stick the 1st 4 bytes at the end
    check = sha256x2(data)
    data.extend(check[0:4])

    # Now we can encode it
    return b58encode(data)

def b58decodecheck(v):
    # Decode everything to get bytes
    full_decode = b58decode(v)

    # Seperate the version|payload from the checksum
    ver_pay = full_decode[0:len(full_decode)-4]
    checksum = full_decode[-4:]

    # Verify the checksum
    check_checksum = sha256x2(ver_pay)[0:4]
    if (checksum != check_checksum):
        logging.error('Invalid b58 encoding %s', v)
        raise ResourceWarning(v)

    # Return the entire payload
    return ver_pay

def __sha256(data):
    return hashlib.sha256(data).digest()

def sha256x2(data):
    return __sha256(__sha256(data))

def __ripemd160(data):
    return hashlib.new("ripemd160", data).digest()

def ripemd160xsha256(data):
    return __ripemd160(__sha256(data))
