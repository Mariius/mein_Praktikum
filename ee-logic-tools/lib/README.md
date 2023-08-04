# Readme of Rohmann's Python Library
Python Library for often used functions. Here are some examples. For more details see python files in main folder.

# file handling
```python
>>> get_version_from_filename('campbell_backplane_c5a4_cpld_0v01.svf')
'0.1.0'
>>> get_version_from_filename('pl650-firmware-1.9.0-487.deb', True)
'1.9.0-487'
>>> get_version_from_filename('a6_32v04.ftdi.svf')
'32.4.0'
>>> read_json_file('test.json')
{...}
>>> get_file_hash('test.json')
'...'
>>> get_file_size('test.json')
15020

```

# type handling
```python

# Check list duplicates
>>> check_for_duplicates([0,1])
False
>>> check_for_duplicates([1,1])
True
# Convert to interger list
>>> convert_to_int_list('0,1')
[0,1]
# Bool handling
>>> convert_bool('true')
True
>>> convert_bool('FALSE')
False
# Slot mask handling
>>> list_to_slot_mask([0,1,2,3,4,5,6,7])
0x00FF
>>> list_to_slot_mask('0,1')
0x0003
>>> slot_mask_to_list(0x00FF)
[0,1,2,3,4,5,6,7]
>>> slot_mask_to_list(0x0003)
[0,1]
```

# bit handling
```python
# Compute the 2's complement of int value val
>>> twos_comp(0xFC, 8)
-4
# Create a binary mask with defined length
>>> create_mask(8)
0xFF
# Swap binary string
>>> swap_bin_str('0b1111101')
'0b1011111'
# Convert integer to binary string
>>> int_to_bin_str(12)
'0b1100'
# Convert hex string to binary string
>>> hex_str_to_bin_str('ab', 8)
'0b10101011'
```

# byte handling
```python
# Hex <> Byte String
>>> hex_to_byte('0x00ffab')
b'\x00\xff\xab'
>>> byte_to_hex(b'\x00\xff\xab')
'0x00ffab'
# DecFloat16 <> Byte String
>>> decfloat16_to_byte(b'\x01\x80')
0.001e-16
>>> decfloat16_to_byte(1e15)
b'\xe8{'
# BFloat16 <> Byte String
>>> bfloat16_to_byte(5000)
b'\x9cE'
>>> byte_to_int(18)
b'\x12'
# Byte Array <> Byte String
>>> bytes_to_byte_list(b'test', 2)
[b'te', b'st']
>>> byte_list_to_bytes([b't', b'e', b's', b't'])
b'test'
```