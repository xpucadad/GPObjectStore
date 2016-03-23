import struct

# difficulty
target = bytearray(b'\x1f\x03\xa3\x0c')
print(target)
print(target.hex())

# extract exponent and convert to an integer
exp_raw = bytearray(target)
exp_raw[1:4] = b'\x00\x00\x00'
print(exp_raw)
exponent = struct.unpack('I', exp_raw)[0] - 3
print(exponent)

# calculate where in the final target the mantissa should start
mantstart = 32 - 3 - exponent # length minus mantissa size minus exponent
print(mantstart)

# load the mantissa into the final target
print(target)
difficulty_target = bytearray(32)
difficulty_target[mantstart:mantstart+3] = target[1:4]

print(difficulty_target, difficulty_target.hex())
full_len = len(difficulty_target)
print(full_len)
