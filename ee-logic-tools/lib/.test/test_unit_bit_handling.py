import unittest

import sys
import os
from pathlib import Path

# >> add folders to syspath
sys.path.insert(0, str(Path(Path(__file__).parent, "..")))
# << add folders to syspath
from bit_handling import bin_to_int, int_to_bin_str
from bit_handling import hex_str_to_bin_str, bin_str_to_hex_str
from bit_handling import swap_bin_str, split_bin_str, split_bin_str_into_chunks, split_hex_str_into_chunks, create_mask
from bit_handling import twos_comp, append_hex

class TestFileHandlingDefault(unittest.TestCase):

    def test_bin_to_int(self):
        a = [1,1,0,1]
        b = bin_to_int(a)
        assert b == 13
    
        a = '1101'
        b = bin_to_int(a)
        assert b == 13
        c = int_to_bin_str(b, start=False)
        assert a == c

        a = '0b1101'
        b = bin_to_int(a)
        assert b == 13
        c = int_to_bin_str(b)
        assert a == c
        
        a = '0b001101'
        b = bin_to_int(a)
        assert b == 13
        c = int_to_bin_str(b,size=6)
        assert a == c
        
        a = '001101'
        b = bin_to_int(a)
        assert b == 13
        c = int_to_bin_str(b,size=6,start=False)
        assert a == c

    def test_swap_bin_str(self):
        a = '11111101'
        b = swap_bin_str(a)
        assert b == '10111111'
        c = swap_bin_str(b)
        assert a == c

        a = '11011101'
        b = swap_bin_str(a)
        assert b == '10111011'    
        c = swap_bin_str(b)
        assert a == c
    
        a = '0b11011101'
        b = swap_bin_str(a)
        assert b == '0b10111011'
        c = swap_bin_str(b)
        assert a == c

    def test_hex_to_bin(self):
        a = '0xff'
        b = hex_str_to_bin_str(a)
        c = bin_str_to_hex_str(b)
        assert b == '0b11111111'
        assert a == c

        a = 'ff'
        b = hex_str_to_bin_str(a)
        c = bin_str_to_hex_str(b, start=False)
        assert b == '0b11111111'
        assert a == c
        
        a = '0xff'
        b = hex_str_to_bin_str(a, 8)
        c = bin_str_to_hex_str(b)
        assert b == '0b11111111'
        assert a == c
        
        a = '0xff'
        b = hex_str_to_bin_str(a, 8, start=False)
        c = bin_str_to_hex_str(b)
        assert b == '11111111'
        assert a == c
        
        a = '0xf'
        b = hex_str_to_bin_str(a, 4)
        c = bin_str_to_hex_str(b)
        assert b == '0b1111'
        assert a == c
        
        a = '0x1'
        b = hex_str_to_bin_str(a, 1)
        c = bin_str_to_hex_str(b)
        assert b == '0b1'
        assert a == c

        a = '0x1'
        b = hex_str_to_bin_str(a, 2)
        c = bin_str_to_hex_str(b)
        assert b == '0b01'
        assert a == c
        
        a = '0x2'
        b = hex_str_to_bin_str(a, 2)
        c = bin_str_to_hex_str(b)
        assert b == '0b10'
        assert a == c
        
    def test_split_bin_str(self):
        assert split_bin_str('1000000111101') == ['1', '0000001', '111', '01']
        assert split_bin_str('000000111101') == ['0000001', '111', '01']
        
    def test_split_bin_str_into_chunks(self):
        assert split_bin_str_into_chunks('1000000111101', 3) == ['100', '000', '011', '110', '1']
        assert split_bin_str_into_chunks('000000111101', 2) == ['00', '00', '00', '11', '11', '01']
        assert split_bin_str_into_chunks('0b000000111101', 2) == ['0b00', '0b00', '0b00', '0b11', '0b11', '0b01']
        assert split_bin_str_into_chunks('0b000000111101', 12) == ['0b000000111101']
        assert split_bin_str_into_chunks('0b000000111101', 13) == ['0b000000111101']
        
    def test_split_hex_str_into_chunks(self):
        assert split_hex_str_into_chunks('aa', 4) == ['a', 'a']
        assert split_hex_str_into_chunks('35', 3) == ['6', '5']
        assert split_hex_str_into_chunks('0x35', 3) == ['0x6', '0x5']
        assert split_hex_str_into_chunks('35', 6) == ['35']
        assert split_hex_str_into_chunks('35', 8) == ['35']
        assert split_hex_str_into_chunks('2abff01bff', size_of_chunks=32, size_of_value=38) == ['aaffc06f', '3f']
        assert split_hex_str_into_chunks('0x2abff01bff', size_of_chunks=32, size_of_value=38) == ['0xaaffc06f', '0x3f']
        
    def test_create_mask(self):
        assert create_mask(1) == 0x1
        assert create_mask(2) == 0x3
        assert create_mask(3) == 0x7
        assert create_mask(4) == 0xF
        assert create_mask(8) == 0xFF
        
    def test_twos_comp(self):
        assert twos_comp(1, 8) == 1
        assert twos_comp(255, 8) == -1
        assert twos_comp(0xFC, 8) == -4     
        
    def test_append_hex(self):
        assert append_hex(0xf, 0xa) == 0xfa
        assert append_hex(0xa, 0x1) == 0x15
        assert append_hex(0xa, 0x1, 4, 2) == 0x29
        assert append_hex('0xa', '0x1', 4, 2) == '0x29'
        assert append_hex('a', '1', 4, 2) == '29'         
        
if __name__ == "__main__":
    unittest.main()
    