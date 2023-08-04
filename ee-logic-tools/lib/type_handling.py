from typing import Union

def list_to_slot_mask(input=None):
    ''' Convert a list to slot mask (zero based)
    
    # Examples
    >>> list_to_slot_mask()
    0xFFFF
    >>> list_to_slot_mask([0,1,2,3,4,5,6,7])
    0x00FF
    >>> list_to_slot_mask([8,9,10,11,12,13,14,15])
    0xFF00
    >>> list_to_slot_mask([1])
    0x0001
    >>> list_to_slot_mask('2')
    0x0004
    >>> list_to_slot_mask('0,1')
    0x0003
    >>> list_to_slot_mask('0, 1')
    0x0003

    '''
    def calc_mask(int_list):
        # calculate output
        val = 0
        for slot in int_list:
            val = val + 2**slot
        return val

    # all
    if input == None:
        return 0xFFFF
    # convert input into a list
    input_converted = convert_to_int_list(input)
    # calculate output
    return calc_mask(input_converted)  

def slot_mask_to_list(input=None):
    ''' Convert a slot mask (zero based) to a list of integers
    
    # Examples
    >>> slot_mask_to_list()
    [0,1,2,3,4,5,6,7,8,10,11,12,13,14,15]
    >>> slot_mask_to_list(0x00FF)
    [0,1,2,3,4,5,6,7]
    >>> slot_mask_to_list(0xFF00)
    [8,9,10,11,12,13,14,15]
    >>> slot_mask_to_list(0x0001)
    [1]
    >>> slot_mask_to_list(0x0004)
    [2]
    >>> slot_mask_to_list(0x0003)
    [0,1]

    '''
    # all
    if input == None:
        input = 0xFFFF
    ret = []
    for i in range(input.bit_length()):
        # shift bit and mask
        if input >> i & 1:
            ret.append(i)
    return ret

def convert_to_int_list(in_value:Union[str,list,int]):
    ''' convert value (int, str or list) to a list of integers '''
    if in_value == None:
        raise ValueError("Your input is a None-type. Please change your input value!")
    if isinstance(in_value, int):
        ret = list()
        ret.append(in_value)
        return ret
    elif isinstance(in_value, str):
        if in_value.startswith('['):
            in_value = in_value[1:]
        if in_value.endswith(']'):
            in_value = in_value[:-1]
        # convert to list
        output = list(map(int, in_value.split(',')))
        # check for duplicates
        if check_for_duplicates(output):
            raise ValueError("Duplicates found in slot list '{}'!".format(in_value))
        return output
    elif isinstance(in_value, list):
        # if input value is a list of strings, convert
        if isinstance(in_value[0], str):
            output = list(map(int, in_value))
            # check for duplicates
            if check_for_duplicates(output):
                raise ValueError("Duplicates found in slot list '{}'!".format(in_value))
            return output
        else:
                # check for duplicates
            if check_for_duplicates(in_value):
                raise ValueError("Duplicates found in slot list '{}'!".format(in_value))
            return in_value

def check_for_duplicates(anylist:list) -> bool:
    ''' check duplicates in a list '''
    if not isinstance(anylist, list):
        return("Error. Passed parameter is Not a list")
    if len(anylist) != len(set(anylist)):
        return True
    else:
        return False

def convert_bool(in_value, dominant=None, raise_error=False):
    ''' convert boolean value - try to convert a value into an bool value
    
    Prameter:  
        with option to set a dominant value:
        - False: in case of in_value does not match with bool values, the return value will be set to true
        - True: in case of in_value does not match with bool values, the return value will be set to true
        - None: in case of in_value does not match with bool values, we will be raise an exception if raise_error is True, else input value will be retunred

    '''
    if in_value == 'true' or in_value == 'True' or in_value == 'TRUE' or in_value == True:
        out_value = True
    elif in_value == 'false' or in_value == 'False' or in_value == 'FALSE' or in_value == False:
        out_value = False
    # in_value does not match with bool value
    else:
        if dominant == True:
            out_value = True
        elif dominant == False:
            out_value = False
        else:  
            if raise_error:
                raise Exception("Unknown input at bool value '{}'. (Expected values: 'true', 'TRUE', 'True', 'false', ...)".format(in_value))
            else:
                out_value = in_value
    return out_value