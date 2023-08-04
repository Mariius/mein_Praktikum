import os
import sys
import numpy as np
import inspect
import logging
from pprint import pprint

from .file_handle import read_json_file

# own definition files
import source.definition_types
import source.vendor_ids
from .byte_handle import byte_to_int, byte_to_bfloat16, bfloat16_to_byte, byte_to_decfloat16, decfloat16_to_byte

class data_structure():
    ''' Data structure for device types: structure of raw data in one-wire-chip
    - Read source/payload_structure json files
    - Validate files
    '''

    def __init__(self) -> None:
        # Setup logging concept
        self.logger = logging.getLogger('data_struct')
        self.logger.setLevel(logging.INFO)

        # define type list, we start with known types
        type_details = [('char[8]', 8), ('char[16]', 16), ('uint8', 1), ('uint16', 2), ('uint32', 4), ('uint8[16]', 16), ('bfloat16', 2), ('decfloat16', 2)]
        # get enum list with length
        enum_length = 1
        enum_details = []
        for enum_type in self._get_definition_type_names():
            enum_details.append((enum_type, enum_length))
        # define type list with byte size as additional information
        self.type_details = type_details + enum_details

        # import
        self.logger.info("Read data structure files.")
        self.device_type = []
        # when file exists: expect normal run
        if os.path.isfile(os.path.join('source', 'structure_payload', 'Booster.json')):
            # self.device_type = self._import(os.path.abspath(os.path.join('source','structure_payload')))
            # self.device_type.append(self._import(os.path.abspath(os.path.join('source','structure_common')))[0]

            self.device_type.append(read_json_file(os.path.abspath(os.path.join('source', 'structure_payload', 'Booster.json'))))
            self.device_type.append(read_json_file(os.path.abspath(os.path.join('source', 'structure_payload', 'Multiplexer.json'))))
            self.device_type.append(read_json_file(os.path.abspath(os.path.join('source', 'structure_payload', 'Rotor.json'))))
            self.device_type.append(read_json_file(os.path.abspath(os.path.join('source', 'structure_payload', 'Sensor.json'))))
            self.device_type.append(read_json_file(os.path.abspath(os.path.join('source', 'structure_common', 'Common.json'))))
        # when file does not exist: expect exe run
        else:
            bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
            print("Temporary folder for windows executable: {}".format(bundle_dir))
            self.device_type.append(read_json_file(os.path.abspath(os.path.join(bundle_dir, 'source', 'structure_payload', 'Booster.json'))))
            self.device_type.append(read_json_file(os.path.abspath(os.path.join(bundle_dir, 'source', 'structure_payload', 'Multiplexer.json'))))
            self.device_type.append(read_json_file(os.path.abspath(os.path.join(bundle_dir, 'source', 'structure_payload', 'Rotor.json'))))
            self.device_type.append(read_json_file(os.path.abspath(os.path.join(bundle_dir, 'source', 'structure_payload', 'Sensor.json'))))
            self.device_type.append(read_json_file(os.path.abspath(os.path.join(bundle_dir, 'source', 'structure_common', 'Common.json'))))
        #pprint(self.device_type)

        # validate
        #self._validate(self.device_type)

    def get_type_length(self, type:str) -> int:
        ''' return int in bytes of type '''
        for name, length in self.type_details:
            if type == name:
                return length
        text = "Type '{}' not in allowed list {}!".format(type, self.get_type_list())
        self.logger.exception(text)
        raise ValueError(text)

    def get_type_list(self) -> list:
        ''' return type list of all types '''
        return [ seq[0] for seq in self.type_details ]

    def _get_definition_type_names(self) -> list:
        ''' get class names of definition_types.py and vendor_ids.py '''
        # init
        ret = []
        # add enums of definition types
        for name, obj in inspect.getmembers(source.definition_types):
            if inspect.isclass(obj):
                ret.append(obj.__name__)
        # add enums of vendir ids
        for name, obj in inspect.getmembers(source.vendor_ids):
            if inspect.isclass(obj):
                ret.append(obj.__name__)

        # # clean up
        # ret.remove('mysql_lib')
        # ret.remove('mysql_lib')

        # return list
        return ret

    def list_device_types(self) -> list:
        ''' list data structure device type '''
        ret = []
        for device_type in self.device_type:
            ret.append(device_type['DeviceType'])
        return ret

    def get_device_type(self, device_type_name: str):
        ''' search device type in data structure '''
        for device_type in self.device_type:
            if device_type_name == device_type['DeviceType']:
                return device_type
        return False

    def get_device_type_payload_length(self, device_type_name: str) -> int:
        ''' get device type payload length in byte '''
        # get payload
        device_type = self.get_device_type(device_type_name)
        # error handling
        if device_type == False:
            text = "Device type '{}' could not be found in device type templates! See folder 'source/..' for details.".format(device_type_name)
            self.logger.exception(text)
            raise TypeError(text)
        else:
            ret = 0
            # get all field information and add type length
            for field in device_type['Raw']:
                ret = ret + self.get_type_length(field['Type'])
            return ret

    def get_device_type_field_names(self, device_type_names, filter:str='Library') -> list:
        ''' get field names matched with library of data structure

        Input:
        - device_type_names str or list
        - filter option

        Example:
            data_struct.get_device_type_field_names(['Common', 'DeviceMultiplexer'])

        data_struct.get_device_type_field_names('Common')
        '''
        ret = []
        
        # handle input: convert it into list
        if isinstance(device_type_names, str):
            device_type_names = [device_type_names]

        for device_type_name in device_type_names:
            # get payload
            device_type = self.get_device_type(device_type_name)
            # error handling
            if device_type == False:
                text = "Device type '{}' could not be found in device type templates! See folder 'source/..' for details.".format(device_type_name)
                self.logger.exception(text)
                raise TypeError(text)
            else:
                # get all fields and return list
                for field in device_type['Raw']:
                    if isinstance(filter,str):
                        if field['Source'] == 'Library':
                            ret.append(field['Field'])
                    else:
                        ret.append(field['Field'])
        return ret

    def get_device_type_field_name_type(self, device_type_names: str, field_name:str) -> str:
        ''' get field names type of data structure

        Example:
        > data_struct.get_device_type_field_name_type(['Common','DeviceMultiplexer'], 'DrvMaxCurrent')
        < uint16
        '''
        # handle input: convert it into list
        if isinstance(device_type_names, str):
            device_type_names = [device_type_names]

        for device_type_name in device_type_names:
            # do dirty hard codes stuff
            if device_type_name == 'DeviceSensor_Coil':
                device_type_name = 'DeviceSensor'
            # get payload
            device_type = self.get_device_type(device_type_name)
            # error handling
            if device_type == False:
                text = "Device type '{}' could not be found in device type templates! See folder 'source/..' for details.".format(device_type_name)
                self.logger.exception(text)
                raise TypeError(text)
            else:
                for field in device_type['Raw']:
                    # filter
                    if field['Field'] == field_name:
                        return field['Type']

    def get_device_type_names_field_name_scaling_factor(self, device_type_names: str, field_name:str) -> float:
        ''' get field names scaling factor of data structure

        Example:
        > data_struct.get_device_type_names_field_name_scaling_factor(['Common','DeviceMultiplexer'], 'DrvMaxCurrent')
        < 10
        '''
        # handle input: convert it into list
        if isinstance(device_type_names, str):
            device_type_names = [device_type_names]

        for device_type_name in device_type_names:
            # do dirty hard codes stuff
            if device_type_name == 'DeviceSensor_Coil':
                device_type_name = 'DeviceSensor'
            # get payload
            device_type = self.get_device_type(device_type_name)
            # error handling
            if device_type == False:
                text = "Device type '{}' could not be found in device type templates! See folder 'source/..' for details.".format(device_type_name)
                self.logger.exception(text)
                raise TypeError(text)
            else:
                for field in device_type['Raw']:
                    # filter
                    if field['Field'] == field_name:
                        if 'ScalingFactor' in field.keys():
                            return field['ScalingFactor']
                        else:
                            return None

    # def get_device_type_field_name_type(self, device_type_name: str, field_name:str) -> str:
    #     ''' get field names type of data structure '''
    #     # get payload
    #     device_type = self.get_device_type(device_type_name)
    #     # error handling
    #     if device_type == False:
    #         text = "Device type '{}' could not be found in device type templates! See folder 'source/..' for details.".format(device_type_name)
    #         self.logger.exception(text)
    #         raise TypeError(text)
    #     else:
    #         for field in device_type['Raw']:
    #             # filter
    #             if field['Field'] == field_name:
    #                 return field['Type']


    def _import(self, folder) -> list:
        ''' Read JSON File(s) '''
        # init return
        ret = []

        # read files from folder
        files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

        for file in files:
            self.logger.info("Read data structure file '{}'.".format(file))

            data = read_json_file(os.path.join(folder, file))

            # add file information
            data['File'] = file

            ret.append(data)

        return ret

    def _validate(self, device_types):
        # validate data structure      
        for device_type in device_types:
            self.logger.info("Validate data structure '{}'.".format(device_type['DeviceType']))        
            # check general stuff
            common_keys = ['DeviceType', 'Description', 'Version', 'CompatibilityVersion', 'Raw']
            for key_to_check in common_keys:
                if key_to_check not in device_type.keys():
                    text = "Check key '{}' not in keys '{}' of device type '{}'. Please edit your json-file '{}'! Neccessary keys are '{}'.".format(key_to_check, device_type.keys(), device_type['DeviceType'], device_type['File'], common_keys)
                    self.logger.exception(text)
                    raise KeyError(text)

            # check special common stuff
            if device_type['DeviceType'] == 'Common':
                if device_type['Version'] != 0:
                    text = "Value of 'Version' '{}' of device type 'Common' is not '0'. Fix this or change this check!".format(device_type['Version'])
                    self.logger.exception(text)
                    raise ValueError(text)
                if device_type['CompatibilityVersion'] != 0:
                    text = "Value of 'CompatibilityVersion' '{}' of device type 'Common' is not '0'. Fix this or change this check!".format(device_type['Version'])
                    self.logger.exception(text)
                    raise ValueError(text)

            # check payload
            for element in device_type['Raw']:
                # check type of every element
                if element['Type'] in self.get_type_list():
                    pass
                else:
                    text = "Type '{}' at field '{}' not in allowed type list {}!".format(element['Type'], element['Field'], self.get_type_list())
                    self.logger.exception(text)
                    raise TypeError(text)
        
        self.logger.info("Validation of data structure successfully finished!")        

        return True

    def convert_from_byte(self, value:bytes, type:str, scaling=1):
        ''' converts from binary string

        Inputs:
            byte        

        Output:
            value: string, int, float, whatever

        '''
        # check input type
        if type not in self.get_type_list():
            text = "Type '{}' not accepted!".format(type)
            self.logger.exception("text")
            raise TypeError(text)
        # set to one
        if scaling == None:
            scaling = 1

        # check value
        if not isinstance(value, bytes) or len(value) != self.get_type_length(type):
            text = "Value '{}' out of type range '{}'!".format(value, type)
            self.logger.exception(text)
            raise ValueError(text)

        # convert data and return
        if type == 'char[8]' or type == 'char[16]':
            # delete trailing zeros
            return value.rstrip(b'\x00').decode()
        elif type == 'uint8' or type == 'uint16' or type == 'uint32':
            value =  byte_to_int(value)
            # scale value
            return value*scaling
        elif type == 'uint8[16]':
            text = "Type '{}' not implemented !".format(type)
            # return [byte_to_int(elem) for elem in value]
        elif type == 'bfloat16':
            value = byte_to_bfloat16(value)
            # scale value
            return value*scaling
        elif type == 'decfloat16':
            value = byte_to_decfloat16(value,'little')
            # scale value
            return value*scaling
        elif type in self._get_definition_type_names():
            if type == 'eDeviceType':
                return source.definition_types.eDeviceType(value).name
            elif type == 'eTriggerType':
                return source.definition_types.eTriggerType(value).name
            elif type == 'eEncoderType':
                return source.definition_types.eEncoderType(value).name
            elif type == 'eInputType':
                return source.definition_types.eInputType(value).name  
            elif type == 'eOutputType':
                return source.definition_types.eOutputType(value).name  
            elif type == 'eCoilType':
                return source.definition_types.eCoilType(value).name  
            elif type == 'fBusType':
                return source.definition_types.fBusType(value).name 
            elif type == 'eVendorId':
                return source.vendor_ids.eVendorId(value).name
            else:
                text = "Type '{}' unknown!".format(type)
                self.logger.exception(text)
                raise TypeError(text)
        else:
            text = "Type '{}' unknown!".format(type)
            self.logger.exception(text)
            raise TypeError(text)

    def convert_to_byte(self, value, type:str, scaling=1, raise_error=True) -> bytes:
        ''' convert to byte string

        Inputs:
            value: string, int, float, whatever
            type (str): char8, char16, uint8, uint16, uint32, decfloat16, bfloat16
            scaling: scale value (library values are si values, the bytes not!)

        Output:
            bytes

        '''
        # check value type
        if type not in self.get_type_list():
            self.logger.error("Type '{}' not accepted!".format(type))
        # set to one
        if scaling == None:
            scaling = 1

        if type == 'char[8]' or type == 'char[16]':
            # check value
            if not isinstance(value, str) or len(value) > self.get_type_length(type):
                text = "Value '{}' out of type range '{}'!".format(value, type)
                if raise_error:
                    self.logger.exception(text)
                    raise ValueError(text)
                else:
                    self.logger.warning(text)
                    return None
            # add trailing zeros
            return value.encode().ljust(self.get_type_length(type), b'\x00')
        elif type == 'uint8' or type == 'uint16' or type == 'uint32':
            # scale value
            fvalue = int(value / scaling)
            # check value
            if not isinstance(fvalue, int) or fvalue < 0 or fvalue >= 2**(self.get_type_length(type)*8):
                if scaling == 1:
                    text = "Value '{}' out of type range '{}'!".format(value, type)
                else:
                    text = "Value '{}/{}={}' is out of type range '{}'!".format(value, scaling, fvalue, type)
                if raise_error:
                    self.logger.exception(text)
                    raise ValueError(text)
                else:
                    self.logger.warning(text)
                    return None
            return fvalue.to_bytes(self.get_type_length(type),'little')
        elif type == 'uint8[16]':
            text = "Type '{}' not implemented !".format(type)
            if raise_error:
                self.logger.exception(text)
                raise ValueError(text)
            else:
                self.logger.warning(text)
                return None
            # # check value
            # if not isinstance(value, int) or value < 0 or value >= 2**16:
            #     text = "Value '{}' out of type range '{}'!".format(value, type)
            #     self.logger.exception(text)
            #     raise ValueError(text)
            # return value.to_bytes(2,'little')
        elif type == 'bfloat16':
            # scale value
            fvalue = value / scaling
            # check value
            if not isinstance(fvalue, float):
                if scaling == 1:
                    text = "Value '{}' out of type range '{}'!".format(value, type)
                else:
                    text = "Value '{}/{}={}' is out of type range '{}'!".format(value, scaling, fvalue, type)
                if raise_error:
                    self.logger.exception(text)
                    raise ValueError(text)
                else:
                    self.logger.warning(text)
                    return None
            return bfloat16_to_byte(fvalue)
        elif type == 'decfloat16':
            # scale value
            fvalue = value / scaling
            # check value
            if not isinstance(value, float):
                if scaling == 1:
                    text = "Value '{}' out of type range '{}'!".format(value, type)
                else:
                    text = "Value '{}/{}={}' is out of type range '{}'!".format(value, scaling, fvalue, type)
                if raise_error:
                    self.logger.exception(text)
                    raise ValueError(text)
                else:
                    self.logger.warning(text)
                    return None
            return decfloat16_to_byte(fvalue,'little')
        elif type in self._get_definition_type_names():
            if type == 'eDeviceType':
                return source.definition_types.eDeviceType[value].value
            elif type == 'eTriggerType':
                return source.definition_types.eTriggerType[value].value
            elif type == 'eEncoderType':
                return source.definition_types.eEncoderType[value].value
            elif type == 'eInputType':
                return source.definition_types.eInputType[value].value  
            elif type == 'eOutputType':
                return source.definition_types.eOutputType[value].value  
            elif type == 'eCoilType':
                return source.definition_types.eCoilType[value].value  
            elif type == 'fBusType':
                return source.definition_types.fBusType[value].value 
            elif type == 'eVendorId':
                return source.vendor_ids.eVendorId[value].value
            else:
                text = "Type '{}' unknown!".format(type)
                if raise_error:
                    self.logger.exception(text)
                    raise ValueError(text)
                else:
                    self.logger.warning(text)
                    return None
        else:
            text = "Type '{}' unknown!".format(type)
            if raise_error:
                self.logger.exception(text)
                raise ValueError(text)
            else:
                self.logger.warning(text)
                return None

# data_struct = payload_structure()
# pprint(data_struct.templates)