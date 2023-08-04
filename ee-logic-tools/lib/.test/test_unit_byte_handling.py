import unittest

import sys
import os
from pathlib import Path

# >> add folders to syspath
sys.path.insert(0, str(Path(Path(__file__).parent, "..")))
# << add folders to syspath

from byte_handling import bfloat16_to_byte, byte_to_bfloat16
from byte_handling import byte_to_hex, hex_to_byte
from byte_handling import bytes_to_byte_list, byte_list_to_bytes
from byte_handling import int_to_byte, byte_to_int
from byte_handling import swap_byte
from byte_handling import decfloat16_to_byte, byte_to_decfloat16
from byte_handling import split_str_into_chunks

class TestFileHandlingDefault(unittest.TestCase):

    def test_bfloat16(self):
        a = 30
        b = bfloat16_to_byte(a)
        assert b == b'\xf0A'
        c = byte_to_bfloat16(b)
        assert a == c

        a = 30.1
        b = bfloat16_to_byte(a)
        assert b == b'\xf0A'
        c = byte_to_bfloat16(b)
        assert c == 30.0
        assert a != c

        a = 5000
        b = bfloat16_to_byte(a)
        assert b == b'\x9cE'
        c = byte_to_bfloat16(b)
        assert c == 4992.0
        assert a != c

    def test_hex_byte(self):
        a = b'\x00\xff\xab'
        b = byte_to_hex(a)
        assert b == '0x00ffab'
        c = hex_to_byte(b)
        assert(a==c)
        
        a = b'\x00\xff\xab'
        b = byte_to_hex(a, start=False)
        assert b == '00ffab'
        c = hex_to_byte(b)
        assert(a==c)

    def test_byte_list(self):
        a = b'test'
        b = bytes_to_byte_list(a)
        assert b == [b't', b'e', b's', b't']
        c = byte_list_to_bytes(b)
        assert a==c

        a = b'test'
        b = bytes_to_byte_list(a, 2)
        assert b == [b'te', b'st']
        c = byte_list_to_bytes(b)
        assert a==c
        
        a = b'test'
        b = bytes_to_byte_list(a, 3)
        assert b == [b'tes', b't']
        c = byte_list_to_bytes(b)
        assert a==c

    def test_int_byte(self):
        a = 256
        b = int_to_byte(a)
        #print(b)
        c = byte_to_int(b)
        assert(a==c)

        a = b'\x12\x8c\x46\xe9\x00\x00\x00\xb9'
        b = byte_to_int(a)
        #print(b)
        c = int_to_byte(b,8)
        assert(a==c)

    def test_swap_byte(self):
        a = b'\x00\xff\xbc\xab'
        b = swap_byte(a)
        assert(a==swap_byte(b))    
    
        a = [b'\x00', b'\xff', b'\xbc', b'\xab']
        b = swap_byte(a)
        assert(a==swap_byte(b))

    def test_decfloat16(self):
        a = 1
        b = decfloat16_to_byte(a)
        #print(byte_to_hex(b))
        c = byte_to_decfloat16(b)
        assert(a==c)

        a = 10e3
        b = decfloat16_to_byte(a)
        #print(byte_to_hex(b))
        c = byte_to_decfloat16(b)
        assert(a==c)

        a = 750e3
        b = decfloat16_to_byte(a)
        #print(byte_to_hex(b))
        c = byte_to_decfloat16(b)
        assert(a==c)

        a = 1e-16
        b = decfloat16_to_byte(a)
        #print(byte_to_hex(b))
        c = byte_to_decfloat16(b)
        assert(a==c)

        a = 0.001e-16
        b = decfloat16_to_byte(a)
        #print(byte_to_hex(b))
        c = byte_to_decfloat16(b)
        assert(a==c)

        a = 1e15
        b = decfloat16_to_byte(a)
        #print(byte_to_hex(b))
        c = byte_to_decfloat16(b)
        assert(a==c)

        a = -1e15
        b = decfloat16_to_byte(a)
        #print(byte_to_hex(b))
        c = byte_to_decfloat16(b)
        assert(a==c)

        a = -20
        b = decfloat16_to_byte(a)
        #print(byte_to_hex(b))
        c = byte_to_decfloat16(b)
        assert(a==c)

        a = 250e4
        b = decfloat16_to_byte(a)
        #print(byte_to_hex(b))
        c = byte_to_decfloat16(b)
        assert(a==c)

        a = None
        b = decfloat16_to_byte(a)
        #print(byte_to_hex(b))
        c = byte_to_decfloat16(b)
        assert(a==c)

        a = 0
        b = decfloat16_to_byte(a)
        #print(byte_to_hex(b))
        c = byte_to_decfloat16(b)
        assert(a==c)
        
    def test_split_str_into_chunks(self):
        a = split_str_into_chunks('Hallo Du da!', 3)
        assert a == ['Hal', 'lo ', 'Du ', 'da!']

        b = split_str_into_chunks('Hallo Du da!', 2)
        assert b == ['Ha', 'll', 'o ', 'Du', ' d', 'a!']      
        
        c = split_str_into_chunks('Hallo Du da!', 12)
        assert c == ['Hallo Du da!']     
        
        d = split_str_into_chunks('Hallo Du da!', 13)
        assert d == ['Hallo Du da!']     

if __name__ == "__main__":
    unittest.main()
    