import numpy
from typing import Union
from bit_handling import twos_comp


def split_str_into_chunks(value:str, size:int) -> list[str]:
    ''' Split string into chunks with defined size
    
    # Parameter
    - value (str): string
    - size (int): size of chunks

    # Examples
    >>> split_str_into_chunks('Hallo Du da!', 3)
    ['Hal', 'lo ', 'Du ', 'da!']

    >>> split_str_into_chunks('Hallo Du da!', 2)
    ['Ha', 'll', 'o ', 'Du', ' d', 'a!']
    '''
    chunks = [value[i:i+size] for i in range(0, len(value), size)]
    return chunks


def byte_to_hex(value:bytes, start:bool=True) -> str:
    ''' Convert byte string into hex string
    
    # Examples
    >>> byte_to_hex(b'\x00\xff\xab')
    '0x00ffab'
    '''
    if start:
        return '0x'+value.hex()
    else:
        return value.hex()

def hex_to_byte(value:str) -> bytes:
    ''' Convert hex string into byte string
    
    # Examples
    >>> hex_to_byte('0x00ffab')
    b'\x00\xff\xab'
    '''
    if value.startswith('0x'):
        return b''.fromhex(value[2:])
    else:
        return b''.fromhex(value)

def byte_list_to_bytes(value:list) -> bytes:
    ''' Convert a list of byte arrays into a byte string
    
    # Examples
    >>> byte_list_to_bytes([b't', b'e', b's', b't'])
    b'test'
    '''
    return b''.join(value)

def bytes_to_byte_list(value:bytes, size:int=1):
    ''' Convert a byte string into a list of byte array

    # Parameter 
    - value (bytes): value to seperate
    - size (int): size in bytes to seperate
    
    # Examples
    >>> bytes_to_byte_list(b'test')
    [b't', b'e', b's', b't']
    >>> bytes_to_byte_list(b'test', 2)
    [b'te', b'st']
    >>> bytes_to_byte_list(b'test', 3)
    [b'tes', b't']
    '''
    return [value[i:i+size] for i in range(0, len(value), size)]

def byte_to_int(value:bytes, byteorder='little', signed=False) -> int:
    ''' Convert a byte string into a integer value

    # Parameter 
    - value (bytes): value to convert
    - byteorder (str): 'little' (default) or 'big'
    - signed (bool): signed value (default False)
    
    # Examples
    >>> byte_to_int(b'\x12'))
    18
    >>> byte_to_int(b'\x00\x12'))
    4608
    '''
    return int.from_bytes(value, byteorder=byteorder, signed=signed)

def int_to_byte(value:int, size=None, byteorder='little', signed=False) -> bytes:
    ''' Convert integer value intp a byte string
    
    # Parameter 
    - value (int): value to convert
    - size (int): in bytes (default None)
    - byteorder (str): 'little' (default) or 'big'
    - signed (bool): signed value (default False)
    
    # Examples
    >>> byte_to_int(18)
    b'\x12'
    >>> byte_to_int(4608)
    b'\x00\x12' 
    '''
    if size == None:
        if value == 0:
            raise Exception("In case of value '0' you have to set a size! Please recall this function with a 'size'!")
        import math
        return value.to_bytes(math.ceil(value.bit_length()/8), byteorder=byteorder, signed=signed)
    else:
        return value.to_bytes(size, byteorder=byteorder, signed=signed)

def swap_byte(value:Union[list, bytes]) -> Union[list, bytes]:
    ''' Swap byte list or byte string '''
    return value[::-1]

def bfloat16_to_byte(value:float) -> bytes:
    ''' Convert a float value (bfloat16 rounded) into a byte string with 16 bit
    bfloat16 using float32 with cutting fraction bits (little)
    
    # Examples
    >>> bfloat16_to_byte(30)
    b'\xf0A'
    >>> bfloat16_to_byte(5000)
    b'\x9cE'
    '''
    value_f32 = numpy.float32(value)
    value_f32_bytes = value_f32.tobytes()
    return value_f32_bytes[2:4]

def byte_to_bfloat16(value:bytes) -> float:
    ''' Convert a byte string into a bfloat16 reduced (16 bit) float value 
    bfloat16 calc using float32 adding fraction bits (little)

    # Examples
    >>> byte_to_bfloat16(b'\xf0A')
    30
    >>> byte_to_bfloat16(b'\x9cE')
    4992.0
    '''
    value_byte = b'\x00\x00' + value
    return numpy.frombuffer(value_byte, dtype='f')[0]

def decfloat16_to_byte(value:float, byteorder='little') -> bytes:
    ''' Convert a decfloat16 into a byte string
        for more details see [confluence](https://rohmann.atlassian.net/wiki/spaces/PROT/pages/157351937/DecFloat16+Format)
    
    # Parameter 
    - value (float): value to convert
    - byteorder (str): 'little' (default) or 'big'
    
    # Examples
    >>> decfloat16_to_byte(1)
    b'\xe8\x03' means 0xe803
    >>> decfloat16_to_byte(10e3)
    b'\xe8#' means 0xe823
    >>> decfloat16_to_byte(750e3)
    b'\xee2' means 0xee32
    >>> decfloat16_to_byte(1e-16)
    b'\xe8\x83' means 0xe883
    >>> decfloat16_to_byte(0.001e-16)
    b'\x01\x80' means 0x0180
    >>> decfloat16_to_byte(1e15)
    b'\xe8{' means 0xe87b
    >>> decfloat16_to_byte(-1e15)
    b'\x18|' means 0x187c
    '''
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
    ''' Convert a byte string into a decfloat16
    for more details see [confluence](https://rohmann.atlassian.net/wiki/spaces/PROT/pages/157351937/DecFloat16+Format)
    
    # Parameter 
    - value (bytes): value to convert
    - byteorder (str): 'little' (default) or 'big'
    
    # Examples
    >>> byte_to_decfloat16(b'\xe8\x03')
    1
    >>> byte_to_decfloat16(b'\xe8#')
    10e3
    >>> decfloat16_to_byte(b'\xee2')
    750e3
    >>> decfloat16_to_byte(b'\xe8\x83')
    1e-16
    >>> decfloat16_to_byte(b'\x01\x80')
    0.001e-16
    >>> decfloat16_to_byte(b'\xe8{')
    1e15
    >>> decfloat16_to_byte(b'\x18|')
    -1e15
    '''
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
