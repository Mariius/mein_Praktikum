from typing import Union

def bin_to_int(value:Union[str, list]) -> int:
    ''' Convert binary string or binary list to integer
    
    # Parameter
    - value: 
      - list of integers with 0 or 1, e.g. [1,1,0,1]
      - string with binary characters '0' or '1', e.g. '1101'
      - binary string with binary characters '0' or '1', e.g. '0b1101'

    # Examples
    >>> bin_to_int([1,1,0,1])
    13
    >>> bin_to_int('1101')
    13
    >>> bin_to_int('0b1101')
    13
    
    '''
    if isinstance(value, str):
        if value.startswith('0b'):
            return int(value,2)
        else:
            return int('0b'+value,2)
    else:
        # for very large lists the following code is faster than "int(value,2)"
        number = 0
        for b in value:
                number = (2 * number) + b
        return number

def int_to_bin_str(value:int, size:int=None, start:bool=True) -> str:
    ''' Convert integer to binary string
    
    # Parameter
    - value: integer, e.g. 12
    - size (int): number of bits (default None)
    - start (bool): if True (default) string sequence '0b' as suffix

    # Examples
    >>> int_to_bin_str(12)
    '0b1100'
    # Examples
    >>> int_to_bin_str(255, start=False)
    '11111111'
    >>> int_to_bin_str(10, size=8)
    '0b00001010'
    >>> int_to_bin_str(191)
    '0b10111111'
    '''
    if size == None:
        if start:
            return bin(value)
        else:    
            return bin(value)[2:]
    else:
        if start:
            return '0b'+bin(value)[2:].zfill(size)
        else:
            return bin(value)[2:].zfill(size)


def hex_str_to_bin_str(value:str, size:int=None, start:bool=True) -> str:
    ''' Convert hex string to binary string

    # Parameter
    - value (str): hex string value (can start with or without '0x')
    - size (int): number of bits (default None)
    - start (bool): if True (default) string sequence '0b' as suffix
    
    # Examples
    >>> hex_str_to_bin_str('ab', 8)
    '0b10101011'
    >>> hex_str_to_bin_str('a', 8)
    '0b0000101'
    '''
    scale = 16
    if size == None:
        if start:
            return bin(int(value, scale))
        else:
            return bin(int(value, scale))[2:]
    else:
        if start:
            return '0b'+bin(int(value, scale))[2:].zfill(size)
        else:
            return bin(int(value, scale))[2:].zfill(size)

def bin_str_to_hex_str(value:str, start:bool=True) -> str:
    ''' Convert binary string to hex string
    
    # Parameter
    - value (str): binary sting (without '0b' at start)
    
    # Examples
    >>> bin_str_to_hex_str('11111111')
    '0xff'
    >>> bin_str_to_hex_str('1010')
    '0xa'
    '''
    if start: 
        return hex(int(value, 2))
    else:
        return hex(int(value, 2))[2:]

def split_hex_str_into_chunks(value:str, size_of_chunks:int, size_of_value:Union[int,None]=None) -> list[str]:
    ''' Split hex string into chunks with defined bit size
    
    # Parameter
    - value (str): hex string (can start with or without '0x')
    - size_of_chunks (int): size of chunks in bits
    - size_of_value (int|None): size of value in bits (if None=default, the value will be calculated by bit_length() of value)
    - raise_error (bool): default

    # Examples
    >>> split_hex_str_into_chunks('aa', 4)
    ['a', 'a']

    >>> split_hex_str_into_chunks('35', 3)
    ['6', '5']
    
    >>> split_hex_str_into_chunks('2abff01bff', size_of_chunks=32, size_of_value=38)
    ['aaffc06f', '3f']
    

    >>> split_hex_str_into_chunks('35', 3)
    ['6', '5']
    '''
    # if value starts with 0x: delete from string and save flag
    start = False
    if value.startswith('0x'):
        value = value[2:]
        start = True
    if size_of_value == None:
        size_of_value = int(value,16).bit_length()
    # convert to binary string
    bin_value = hex_str_to_bin_str(value=value, size=size_of_value, start=False)
    # convert to bin chunks
    bin_chunks = split_bin_str_into_chunks(value=bin_value, size=size_of_chunks)
    # convert bin chunks to hex chunks
    chunks = [bin_str_to_hex_str(bin_chunk, start=start) for bin_chunk in bin_chunks]
    return chunks

def swap_bin_str(value:str) -> str:
    ''' Swap binary string
    
    # Parameter
    - value: string (can start with or without '0b')

    # Examples
    >>> swap_bin_str('1111101')
    '1011111'
    >>> swap_bin_str('0b1111101')
    '0b1011111'
    '''
    if value.startswith('0b'):
        return '0b'+value[:-len(value)+1:-1]
    else:
        return value[::-1]

def split_bin_str_into_chunks(value:str, size:int) -> list[str]:
    ''' Split binary string into chunks with defined bit size
    
    # Parameter
    - value (str): bit string (can start with or without '0b')
    - size (int): size of chunks in bits

    # Examples
    >>> split_bin_str_into_chunks('1000000111101', 3)
    ['100', '000', '011', '110', '1']

    >>> split_bin_str_into_chunks('000000111101', 2)
    ['00', '00', '00', '11', '11', '01']
    
    >>> split_bin_str_into_chunks('0b000000111101', 2)
    ['0b00', '0b00', '0b00', '0b11', '0b11', '0b01']
    '''
    # if value starts with 0b: delete from string and save flag
    start = False
    if value.startswith('0b'):
        value = value[2:]
        start = True
    chunks = [value[i:i+size] for i in range(0, len(value), size)]
    # if value started with 0b: add to every chuck 0b
    if start:
        chunks = ['0b'+chunk for chunk in chunks]
    return chunks

def split_bin_str(value:str) -> list[str]:
    ''' Split binary string into sequences
    
    Needed to manipulate jtag sequences 

    # Parameter
    - value: string (can start with or without '0b')

    # Examples
    >>> split_bin_str('1000000111101')
    ['1', '0000001', '111', '01']

    >>> split_bin_str('000000111101')
    ['0000001', '111', '01']
    '''
    # init output
    output = ['']
    # init next split flag
    split_on_next = False
    # init split index
    split_index = 0
    # read input lengt
    input_length = len(value)
    # loop over all values
    for i in range(len(value)):
        # add to current splitted
        output[split_index] += value[i]
        # if not the end reached
        if i < input_length-1:
            if split_on_next == True:
                # split: increment index
                split_index += 1
                output.append('')
                # reset flag
                split_on_next = False
            # if next sign is not equal to the current sign
            elif value[i] != value[i+1]:
                # in case of a 0 section add the next tms 1 to the current section and set the flag to split on next time
                if value[i] == '0' and value[i+1] == '1':
                    split_on_next = True
                else:
                    # split: increment index
                    split_index += 1
                    output.append('')
    return output

def create_mask(length:int):
    ''' Create a binary mask with defined length
    
    # Example
    >>> create_mask(1)
    0x1
    >>> create_mask(2)
    0x3
    >>> create_mask(3)
    0x7
    >>> create_mask(8)
    0xFF
    '''
    # input check
    if isinstance(length, str):
        raise ValueError("Invalid length value. Your length value is a string!")
    elif not isinstance(length, int):
        raise ValueError("Invalid length value. Only integers allowed!")
    elif length <= 0:
        raise ValueError("Invalid length value. Only integers greater than 0 allowed!")
    # calc return value
    return int('1'*length, 2)

def twos_comp(val:int, bits:int) -> int:
    ''' Compute the 2's complement / twoes complement of int value val
    
    # Parameter
    - val (int): value, e.g. 12
    - bits (int): number of bits
    
    # Examples
    >>> twos_comp(12, 8)
    12
    >>> twos_comp(255, 8)
    -1
    >>> twos_comp(0xFC, 8)
    -4
    '''
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val   

def append_hex(a:Union[int,str], b:Union[int,str], len_a:int=None, len_b:int=None, ret_len:bool=False):
    ''' Append hex values together
    
    # Parameter
    - a (int or str): first value as hex, e.g. 0x29, '0x29', '29'
    - b (int or str): second value as hex, e.g. 0x18, '0x18', '18'
    - len_a (int): length in bits of value a
    - len_b (int): length in bits of value b
    - ret_len (bool): return length
        
    # Examples
    >>> append_hex(0xf, 0xa))
    0xfa
    >>> append_hex(0xa, 0x1)
    0x15
    >>> append_hex(0xa, 0x1, 4, 2))
    0x29
    >>> append_hex('0xa', '0x1', 4, 2))
    '0x29'
    >>> append_hex('a', '1', 4, 2))
    '29'
    '''
    # input management
    string = False
    start = False
    if isinstance(a, str) ^ isinstance(a, str):
        raise ValueError("Only one value is a string value!")
    elif isinstance(a, str) and isinstance(a, str):
        string = True
        if a.startswith('0x') ^ a.startswith('0x'):
            raise ValueError("Only one value starts with '0x'!")
        elif a.startswith('0x') and a.startswith('0x'):
            start = True
        # convert to integer values
        a = int(a,16)
        b = int(b,16)
    if len_a == None:
        len_a = a.bit_length()
    else:
        if len_a < a.bit_length():
            raise ValueError("Wrong bit size for value a! Needed bit size is '{}', your input is '{}'.".format(a.bit_length(), len_a))
    if len_b == None:
        len_b = b.bit_length()
    else:
        if len_b < b.bit_length():
            raise ValueError("Wrong bit size for value b! Needed bit size is '{}', your input is '{}'.".format(b.bit_length(), len_b))
    if string:
        if start:
            if ret_len:
                return hex((a<<len_b)|b), len_a+len_b
            else:
                return hex((a<<len_b)|b)
        else:
            if ret_len:
                return hex((a<<len_b)|b)[2:], len_a+len_b
            else:
                return hex((a<<len_b)|b)[2:]
    if ret_len:
        return (a<<len_b)|b, len_a+len_b
    else:
        return (a<<len_b)|b
