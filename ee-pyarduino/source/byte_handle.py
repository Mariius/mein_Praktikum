from logging import exception
import numpy
import math

from numpy.core.numeric import NaN

def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val    

def byte_to_hex(value:bytes) -> str:
    return value.hex()

def hex_to_byte(value:str) -> bytes:
    return b''.fromhex(value)

def byte_list_to_bytes(value:list) -> bytes:
    return b''.join(value)

def bytes_to_byte_list(value:bytes, size:int=1):
    return [value[i:i+size] for i in range(0, len(value), size)]

def byte_to_int(value: bytes, byteorder='little', signed=False) -> int:
    return int.from_bytes(value, byteorder=byteorder, signed=signed)

def int_to_byte(value:int, size=None, byteorder='little', signed=False) -> bytes:
    '''
        size in bytes
        byteorder 'little' or 'big'
        signed False or True
    '''
    if size == None:
        if value == 0:
            raise Exception("In case of value '0' you have to set a size! Please recall this function with a 'size'!")
        import math
        return value.to_bytes(math.ceil(value.bit_length()/8), byteorder=byteorder, signed=signed)
    else:
        return value.to_bytes(size, byteorder=byteorder, signed=signed)

def swap_byte_list(value:list) -> list:
    #value.reverse()
    return value[::-1]

def swap_byte(value:bytes) -> bytes:
    return value[::-1]

def bfloat16_to_byte(value:float) -> bytes:
    ''' bfloat16 calc using float32 with cutting fraction bits (little)'''
    value_f32 = numpy.float32(value)
    value_f32_bytes = value_f32.tobytes()
    return value_f32_bytes[2:4]

def byte_to_bfloat16(value:bytes) -> float:
    ''' bfloat16 calc using float32 adding fraction bits (little)'''
    value_byte = b'\x00\x00' + value
    return numpy.frombuffer(value_byte, dtype='f')[0]

def decfloat16_to_byte(value:float, byteorder='little') -> bytes:
    ''' decfloat16 calc '''
    if value == None:
        return b'\xff\xff'
    # handle exponent calc with negative values
    if value == 0:
        exp = 0
    elif value < 0:
        exp = int(numpy.ceil(numpy.log10(-value)))
    else:
        exp = int(numpy.ceil(numpy.log10(value)))
    # check maxmimum value
    if exp > 15:
        raise ValueError("Exponent error: Number is too big! Please select a number with maximum exponent of 15.")
    if exp < -16:
        if value < 1e-19:
            raise ValueError("Exponent error: Number is too small! Please select a number with minimum exponent of -16. wiht value = 0.001")
        exp = -16
    exp_val = exp << 11
    mant = value/10**exp
    mant_val = int(mant*1000)
    ret_val = (exp_val | (mant_val & 0x7FF)) & 0xFFFF
    # print("exp: {}".format(exp))
    # print("exp_val: {} ({})".format(exp_val, hex(exp_val)))
    # print("mant: {}".format(mant))
    # print("mant_val: {} ({})".format(mant_val, hex(mant_val)))
    # print("bytes: ({})".format(hex(ret_val)))
    return int_to_byte(ret_val, size=2, byteorder=byteorder, signed=False)

def byte_to_decfloat16(value:bytes, byteorder='little') -> float:
    ''' decfloat16 calc (little)'''
    if value == b'\xff\xff':
        return None
    value_int = byte_to_int(value, byteorder=byteorder)
    #print(value_int)
    exp = int((value_int >> 11) & 0x1F)
    # negative exponent
    if (exp > 15):
        exp = twos_comp(exp, 5)
    mant = int(value_int & 0x7FF)
    # negative mantisse
    if (mant > 0x3FF):
        mant = twos_comp(mant, 11)
    # print("exp: {} ({})".format(exp, hex(exp)))
    # print("mant: {} ({})".format(int(mant/1000), hex(int(mant/1000))))
    return (mant/1000) * 10**exp

# # section four two
# print('\nsection four two')
# a = 0.001e-16
# print(a)
# b = decfloat16_to_byte(a)
# print(byte_to_hex(b))
# c = byte_to_decfloat16(b)
# print(c)

# # section one
# print("section one")
# a = 1
# print(a)
# b = decfloat16_to_byte(a)
# print(byte_to_hex(b))
# c = byte_to_decfloat16(b)
# print(c)

# # section two
# print("section two")
# a = 10e3
# print(a)
# b = decfloat16_to_byte(a)
# print(byte_to_hex(b))
# c = byte_to_decfloat16(b)
# print(c)

# # section three
# print("section three")
# a = 750e3
# print(a)
# b = decfloat16_to_byte(a)
# print(byte_to_hex(b))
# c = byte_to_decfloat16(b)
# print(c)

# # section four
# print("section four")
# a = 1e-16
# print(a)
# b = decfloat16_to_byte(a)
# print(byte_to_hex(b))
# c = byte_to_decfloat16(b)
# print(c)

# # section five
# print("section five")
# a = 1e15
# print(a)
# b = decfloat16_to_byte(a)
# print(byte_to_hex(b))
# c = byte_to_decfloat16(b)
# print(c)

# # section six
# print("section six")
# a = -20
# print(a)
# b = decfloat16_to_byte(a)
# print(byte_to_hex(b))
# c = byte_to_decfloat16(b)
# print(c)

# # section one
# print("section one")
# a = 30
# print(a)
# b = bfloat16_to_byte(a)
# print(b)
# c = byte_to_bfloat16(b)
# print(c)

# # section two
# print("section two")
# a = 30.1
# print(a)
# b = bfloat16_to_byte(a)
# print(b)
# c = byte_to_bfloat16(b)
# print(c)

# # section three
# print("section three")
# a = 5000
# print(a)
# b = bfloat16_to_byte(a)
# print(b)
# c = byte_to_bfloat16(b)
# print(c)

# # section one
# print('\nsection one')
# a = b'\x00\xff\xab'
# print(a)
# b = byte_to_hex(a)
# print(b)
# c = hex_to_byte(b)
# print(c)

# # section two
# print('\nsection two')
# a = b'test'
# print(a)
# b = bytes_to_byte_list(a)
# print(b)
# c = byte_list_to_bytes(b)
# print(c)

# # section three
# print('\nsection three')
# a = 256
# print(a)
# b = int_to_byte(a)
# print(b)
# c = byte_to_int(b)
# print(c)

# # section four
# print('\nsection four')
# a = b'\x00\xff\xbc\xab'
# print(a)
# b = swap_byte(a)
# print(b)

# # section five
# print('\nsection five')
# a = [b'\x00', b'\xff', b'\xbc', b'\xab']
# print(a)
# b = swap_byte_list(a)
# print(b)

# # section six
# a = b'\x12\x8c\x46\xe9\x00\x00\x00\xb9'
# print(a)
# b = byte_to_int(a)
# print(b)
# c = int_to_byte(b,8)
# print(c)