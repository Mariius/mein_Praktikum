from datetime import datetime

from enum import Enum
from pprint import pprint

from source.library_base import mysql_lib_base


class AdvancedEnum(Enum):
    ''' a advanced enum with options '''
    @classmethod
    def has_key(cls, key):
        ''' returns True if enum has the special key '''
        return key in cls.__members__

    @classmethod
    def keys(cls):
        ''' answer with the list of keys '''
        return list(cls.__members__.keys())

    def equals(self, string):
        ''' returns True if the name of the enum matches '''
        return self.name == string

# Singelton helper class
class _mysql_lib(mysql_lib_base):
    ''' library class advanced

    handle libary specific stuff
    '''

    def __init__(self, user='onewire', password='fanta', host='build.rohmann.de', port='3306', database='one-wire'):    #host='build.rohmann.de' or host='10.10.103.15'
        ''' init '''
        # just for the sake of information
        self.instance = "Instance at %d" % self.__hash__()

        # init class
        super().__init__(user=user, password=password, host=host, port=port, database=database)
        # add table list
        self.table_definition = [
                {
                    'view': 'DeviceSensor',
                    'type': 'device',
                    'tables':[
                        {'name':'device', 'type':'device', 'level':'top', 'link_to_level_above': 'CommonId'},
                        {'name':'device_sensor', 'type':'sensor', 'level':'middle', 'link_to_level_above': 'DeviceId'},
                        {'name':'device_sensor_coil', 'type':'coil', 'level':'bottom', 'link_to_level_above': 'SubId', 'key':'ElementType'}
                    ]
                },
                {
                    'view': 'DeviceSensor_Coil',
                    'type': 'sub',
                    'link': ['DeviceSensor'],
                    'tables':[
                        {'name':'device_sensor_coil', 'type':'coil', 'level':'bottom', 'link_to_level_above': 'SubId', 'key':'ElementType'}
                    ]
                },
                {
                    'view': 'DeviceRotor',
                    'type': 'device',
                    'tables':[
                        {'name':'device', 'type':'device', 'level':'top', 'link_to_level_above': 'CommonId'},
                        {'name':'device_rotor', 'type':'rotor', 'level':'middle', 'link_to_level_above': 'DeviceId'}
                    ]
                },
                {
                    'view': 'DeviceMultiplexer',
                    'type': 'device',
                    'tables':[
                        {'name':'device', 'type':'device', 'level':'top', 'link_to_level_above': 'CommonId'},
                        {'name':'device_multiplexer', 'type':'multiplexer', 'level':'middle', 'link_to_level_above': 'DeviceId'}
                    ]
                }
            ]
        #self.__init_table_definition()

    def __call__(self):
        return self

    def close(self):
        ''' close connection'''
        #super().close()

    def init(self):
        # validate database
        #self._validate()
        pass
    
    # def __init_table_definition(self):
    #     ''' add attributes to table definition '''
    #     # init
    #     #top_table = None
    #     middle_table = None
    #     bottom_table = None
    #     # add data to table definition
    #     for view_struct in self.table_definition:
    #         # get table names for level
    #         for table in view_struct['tables']:
    #             if table['level'] == 'top':
    #                 #top_table = table
    #                 pass
    #             elif table['level'] == 'middle':
    #                 middle_table = table
    #             elif table['level'] == 'bottom':
    #                 bottom_table = table
    #             else:
    #                 text = "level '{}' not implemented, yet.".format(table['level'])
    #                 self.logger.exception(text)
    #                 raise Exception(text)
    #         # set data
    #         for table in view_struct['tables']:
    #             if table['level'] == 'top':
    #                 table['link_to_level_below'] = middle_table['link_to_level_above']
    #             elif table['level'] == 'middle':
    #                 table['link_to_level_below'] = bottom_table['link_to_level_above']
    #             elif table['level'] == 'bottom':
    #                 table['link_to_level_below'] = None
    #             else:
    #                 text = "level '{}' not implemented, yet.".format(table['level'])
    #                 self.logger.exception(text)
    #                 raise Exception(text)

    def _get_definition_tables_linked(self, dev_type:str, level:str, pointer='top'):
        ''' return link to level by device type (view) and level
        pointer = 'top' or 'down'
        '''
        name = None
        linked_name = None
        link = None
        # read data from table definition
        for view_struct in self.table_definition:
            if view_struct['view'] == dev_type:
                # get table names for level
                for table in view_struct['tables']:
                    if table['level'] == level:
                        name = table['name']
                        if pointer == 'top':
                            link = table['link_to_level_above']
                    if pointer == 'top':        
                        if level == 'middle' and table['level'] == 'top':
                            linked_name = table['name']
                        if level == 'bottom' and table['level'] == 'middle':
                            linked_name = table['name']
                    elif pointer == 'down':
                        if level == 'top' and table['level'] == 'middle':
                            linked_name = table['name']
                            link = table['link_to_level_above']
                        if level == 'middle' and table['level'] == 'bottom':
                            linked_name = table['name']
                            link = table['link_to_level_above']
                    else: 
                        text = "Unknown pointer '{}'".format(pointer)
                        self.logger.exception(text) 
                        raise ValueError(text)
                break        
                
        # if nothing found, return none
        return name, linked_name, link

    def _get_definition_type_by_view(self, dev_type:str):
        ''' return definiton type by view '''
        # read data from table definition
        for view_struct in self.table_definition:
            if view_struct['view'] == dev_type:
                # return type
                return view_struct['type']
        # if nothing found
        text = "Unknown device type!".format(dev_type)
        self.logger.exception(text)
        raise Exception(text)

    def _get_definition_link_by_view(self, dev_type:str):
        ''' return definiton link by view '''
        # read data from table definition
        for view_struct in self.table_definition:
            if view_struct['view'] == dev_type:
                # return link
                return view_struct['link']
        # if nothing found
        text = "Unknown device type!".format(dev_type)
        self.logger.exception(text)
        raise Exception(text)

    def _get_definition_tables_by_view(self, dev_type:str):
        ''' return table names by device type (view) '''
        # read data from table definition
        for view_struct in self.table_definition:
            if view_struct['view'] == dev_type:
                # return tables
                return view_struct['tables']
        # if nothing found
        text = "Unknown device type '{}'!".format(dev_type)
        self.logger.exception(text)
        raise Exception(text)

    def _list_all_definition_tables(self):
        ''' return table names and the type '''
        # init returns
        return_tables = []

        # read data from table definition
        for view_struct in self.table_definition:
            # get table names for level level
            for table in view_struct['tables']:
                if table['name'] not in [i[0] for i in return_tables]:                   
                    return_tables.append((table['name'], table['type']))
        return return_tables

    def _validate(self) -> bool:
        ''' validate total database
        iterate over all tables
        '''
        # style: table_list [(table_name, table_type), ...]
        table_list = self._list_all_definition_tables()

        for (table_name, table_type) in table_list:
            self.logger.info("Validate library content of table '{}'.".format(table_name))
            table = self._get_table_data(table_name)
            for row in table:
                self.__validate(row, table_type)

        self.logger.info("Validation of library content successfully finished!")

    def __validate(self, row:dict, table_type:str):
        ''' validate different table types
        this function raise an exeption on error
        '''
        if table_type == 'coil':
            if row['SubId'] not in self._get_table_column_data('device_sensor','SubId'):
                self.logger.warning("SubId '{}' with ElementType '{}' is not used in table '{}'! ".format(row['SubId'],row['ElementType'], 'device_sensor'))
            if row['RecACoilType'] not in self.get_enum('eCoilType').keys():
                text = "Wrong Enum Element selected at key '{}' at row '{}'!".format('RecACoilType', row['ElementType'])
                self.logger.exception(text)
                raise ValueError(text)   
            if row['RecBCoilType'] not in self.get_enum('eCoilType').keys():
                text = "Wrong Enum Element selected at key '{}' at row '{}'!".format('RecBCoilType', row['ElementType'])
                self.logger.exception(text)
                raise ValueError(text)   
            if row['FrequencyLow'] > row['Frequency']:
                text = "Min. frequency'{}' is greater than nominal frequency '{}' at row '{}'!".format(row['FrequencyLow'], row['Frequency'], row['ElementType'])
                self.logger.exception(text)
                raise ValueError(text)                   
            if row['Frequency'] > row['FrequencyHigh']:
                text = "Nominal frequency '{}' is greater than max. frequency '{}' at row '{}'!".format(row['Frequency'], row['FrequencyHigh'], row['ElementType'])
                self.logger.exception(text)
                raise ValueError(text)                   
        elif table_type == 'sensor':    
            if row['SubId'] not in self._get_table_column_data('device_sensor_coil','SubId'):
                text = "SubId '{}' is not in table '{}'! ".format(row['SubId'], 'device_sensor_coil')
                self.logger.exception(text)
                raise ValueError(text)     
            if row['DeviceId'] not in self._get_table_column_data('device','DeviceId',"DeviceType='DeviceSensor'"):
                self.logger.warning("DeviceId '{}' of 'DeviceSensor' is not used in table '{}'! ".format(row['DeviceId'], 'device'))
        elif table_type == 'rotor': 
            if row['TriggerType'] not in self.get_enum('eTriggerType').keys():
                text = "Wrong Enum Element selected at key '{}' at row '{}'!".format('TriggerType', row['RotorType'])
                self.logger.exception(text)
                raise ValueError(text)                   
            if row['EncoderTypeX'] not in self.get_enum('eEncoderType').keys():
                text = "Wrong Enum Element selected at key '{}' at row '{}'!".format('EncoderTypeX', row['RotorType'])
                self.logger.exception(text)
                raise ValueError(text)                   
            if row['EncoderTypeY'] not in self.get_enum('eEncoderType').keys():
                text = "Wrong Enum Element selected at key '{}' at row '{}'!".format('EncoderTypeY', row['RotorType'])
                self.logger.exception(text)
                raise ValueError(text)                   
            if row['MinVoltage'] > row['NomVoltage']:
                text = "Min. voltage '{}' is greater than nominal voltage '{}' at row '{}'!".format(row['MinVoltage'], row['NomVoltage'], row['RotorType'])
                self.logger.exception(text)
                raise ValueError(text)                   
            if row['NomVoltage'] > row['MaxVoltage']:
                text = "Nominal voltage '{}' is greater than max. voltage '{}' at row '{}'!".format(row['NomVoltage'], row['MaxVoltage'], row['RotorType'])
                self.logger.exception(text)
                raise ValueError(text)                   
            if row['MinRPM'] > row['NomRPM']:
                text = "Min. RPM '{}' is greater than nominal RPM '{}' at row '{}'!".format(row['MinRPM'], row['NomRPM'], row['RotorType'])
                self.logger.exception(text)
                raise ValueError(text)                   
            if row['NomRPM'] > row['MaxRPM']:
                text = "Nominal RPM '{}' is greater than max. RPM '{}' at row '{}'!".format(row['NomRPM'], row['MaxRPM'], row['RotorType'])
                self.logger.exception(text)
                raise ValueError(text)     
            if row['DeviceId'] not in self._get_table_column_data('device','DeviceId',"DeviceType='DeviceRotor'"):
                self.logger.warning("DeviceId '{}' of 'DeviceRotor' is not used in table '{}'! ".format(row['DeviceId'], 'device'))              
        elif table_type == 'multiplexer': 
            if row['RecAInput'] not in self.get_enum('eInputType').keys():
                text = "Wrong Enum Element selected at key '{}' at row '{}'!".format('RecAInput', row['MuxDescription'])
                self.logger.exception(text)
                raise ValueError(text)                   
            if row['RecBInput'] not in self.get_enum('eInputType').keys():
                text = "Wrong Enum Element selected at key '{}' at row '{}'!".format('RecBInput', row['MuxDescription'])
                self.logger.exception(text)
                raise ValueError(text)                   
            if row['RecAOutput'] not in self.get_enum('eOutputType').keys():
                text = "Wrong Enum Element selected at key '{}' at row '{}'!".format('RecAOutput', row['MuxDescription'])
                self.logger.exception(text)
                raise ValueError(text)                   
            if row['RecBOutput'] not in self.get_enum('eOutputType').keys():
                text = "Wrong Enum Element selected at key '{}' at row '{}'!".format('RecBOutput', row['MuxDescription'])
                self.logger.exception(text)
                raise ValueError(text)                   
            if row['Encoder'] not in self.get_enum('eEncoderType').keys():
                text = "Wrong Enum Element selected at key '{}' at row '{}'!".format('Encoder', row['MuxDescription'])
                self.logger.exception(text)
                raise ValueError(text)         
            if row['DeviceId'] not in self._get_table_column_data('device','DeviceId',"DeviceType='DeviceMultiplexer'"):
                self.logger.warning("DeviceId '{}' of 'DeviceMultiplexer' is not used in table '{}'! ".format(row['DeviceId'], 'device'))             
        elif table_type == 'device': 
            if row['DeviceType'] not in self.get_enum('eDeviceType').keys():
                text = "Wrong Enum Element selected at key '{}' at row '{}'!".format('DeviceType', row['OrderCode'])
                self.logger.exception(text)
                raise ValueError(text)                   
            if row['DeviceType'] == 'DeviceSensor':
                if row['DeviceId'] not in self._get_table_column_data('device_sensor','DeviceId'):
                    text = "DeviceId '{}' is not in table '{}'! ".format(row['DeviceId'], 'device_sensor')
                    self.logger.exception(text)
                    raise ValueError(text)                       
            elif row['DeviceType'] == 'DeviceMultiplexer':
                if row['DeviceId'] not in self._get_table_column_data('device_multiplexer','DeviceId'):
                    text = "DeviceId '{}' is not in table '{}'! ".format(row['DeviceId'], 'device_multiplexer')
                    self.logger.exception(text)
                    raise ValueError(text)                       
            elif row['DeviceType'] == 'DeviceRotor':
                if row['DeviceId'] not in self._get_table_column_data('device_rotor','DeviceId'):
                    text = "DeviceId '{}' is not in table '{}'! ".format(row['DeviceId'], 'device_rotor')
                    self.logger.exception(text)
                    raise ValueError(text)                       
        else:
            text = "Unknown table_type '{}'!".format(table_type)
            self.logger.exception(text)
            raise ValueError(text)    

    def get_enum(self, def_type:str) -> AdvancedEnum:
        ''' return advanced enum of a defintion type '''

        # evaluate input
        if def_type == 'eDeviceType':
            table = 'definition_type_device'
        elif def_type == 'eCoilType':            
            table = 'definition_type_coil'
        elif def_type == 'eTriggerType':            
            table = 'definition_type_trigger'
        elif def_type == 'eInputType':            
            table = 'definition_type_input'
        elif def_type == 'eOutputType':            
            table = 'definition_type_output'
        elif def_type == 'eEncoderType':            
            table = 'definition_type_encoder'
        elif def_type == 'fBusType':            
            table = 'definition_type_bustype'
        elif def_type == 'eVendorId':            
            table = 'vendor_id'
        else:
            text = "Unknown definition type: '{}'!".format(def_type)
            self.logger.exception(text)
            raise ValueError(text)   

        # get table from database
        table = self._get_table_data(table)
        # create empyt dict
        return_dict = {}
        # step over table and generate new data format with convertion of id
        for element in table:
            return_dict[element['name']] = element['value'].to_bytes(1,'little')
            #return_dict[element['name']] = element['value']
        # return special enum
        return AdvancedEnum(def_type, return_dict)

    def get_vendor_id(self):
        ''' return enum of vendor id '''
        return self.get_enum('eVendorId')

    def remove_device(self, dev_type:str, id:int):
        ''' remove library content by device type and id '''    

        # get type information of view
        type = self._get_definition_type_by_view(dev_type)

        # in case of a sub view
        if type == 'sub': 
            # get table and identifier
            table_name_sub, _, identfier = self._get_definition_tables_linked(dev_type, level='bottom')
            # prepare where for selected device
            where = "{}={}".format(identfier, id)
            # check if id exists
            if self._get_table_data(table_name_sub, where) == []:
                self.logger.error("Id '{}' does not exist in table '{}'. Cant't delete.".format(table_name_sub, id))
                return False

            # check if sub device is used anywhere!
            linked_views = self._get_definition_link_by_view(dev_type)
            for linked_view in linked_views:
                device_list = self.list_device(linked_view)
                for device in device_list:
                    if device[identfier] == int(id):
                        self.logger.error("Sub device '{}' is used in device '{}'. Please delete this device first. Than delete the sub device!".format(id, device['OrderCode']))
                        return False 

            # when existing and not used anywhere, delete
            self._delete_table_data(table_name_sub, where)
            return True
        # in case of normal device
        elif type == 'device': 
            # get table and identifier
            table_name_common, _, top_identfier = self._get_definition_tables_linked(dev_type, level='top', pointer='top')
            table_name_device, table_name_common, middle_identfier = self._get_definition_tables_linked(dev_type, level='middle', pointer='top')
            table_name_sub, table_name_device, bottom_identfier = self._get_definition_tables_linked(dev_type, level='bottom', pointer='top')

            # prepare where for selected device
            where = "{}={}".format(top_identfier, id)
            # get common data
            common_device = self._get_table_data(table_name_common, where)
            # delete from common data
            self._delete_table_data(table_name_common, where)
            self.logger.info("Delete device id '{}' from table '{}'.".format(id, common_device))

            # prepare where for other devices
            # get table and identifier
            dev_id = common_device[0][middle_identfier]
            where = "{}={} and DeviceType='{}'".format(middle_identfier, dev_id, dev_type)
            # get common data
            common_device_other = self._get_table_data(table_name_common, where)
            # get device data
            where = "{}='{}'".format(middle_identfier, dev_id)
            device = self._get_table_data(table_name_device, where)

            # check if device id is used in another device
            # if not, delete
            if common_device_other == []:
                # prepare where
                where = "{}='{}'".format(middle_identfier, dev_id)
                self._delete_table_data(table_name_device, where)
                self.logger.info("Delete also device id '{}' from table '{}'.".format(dev_id, table_name_device))

            # if sub exists:
            if table_name_sub != None:
                sub_id = device[0][bottom_identfier]
                where = "{}='{}'".format(bottom_identfier, sub_id)
                device_other = self._get_table_data(table_name_device, where)
                # check if sub id is used in another device
                # if not, delete
                if device_other == []:
                    # prepare where
                    where = "{}='{}'".format(bottom_identfier, sub_id)
                    self._delete_table_data(table_name_sub, where)
                    self.logger.info("Delete also element type '{}' from table '{}'.".format(sub_id, table_name_sub))
            return True       
        else:
            text = "Definition type '{}' is unsupported".format(type)
            self.logger.exception(text)
            raise ValueError(text)

    def list_library_comments(self, dev_type:str) -> list:
        ''' return list of a device types (with common stuff e.g. order code, ...) '''
        ret = []
        # evaluate input
        tables = self._get_definition_tables_by_view(dev_type)
        for table in tables:
            ret = ret + self._get_table_column_keys_and_comments(table['name'])
        return ret

    def list_device_type_info(self, dev_type:str) -> list:
        ''' return list of dicts of a device types (without common stuff e.g. order code, ...)
        '''
        # init empty where
        where = ''
        # get type of view
        type = self._get_definition_type_by_view(dev_type)
        # get table info
        if type == 'device':
            own_table, link_table, link = self._get_definition_tables_linked(dev_type, level='middle', pointer='down')
        elif type == 'sub':
            own_table, link_table, link = self._get_definition_tables_linked(dev_type, level='bottom')
        else:
            text = "Definition type '{}' is unsupported".format(type)
            self.logger.exception(text)
            raise ValueError(text)

        # in case of a single table
        if link_table == None:
            table_name = own_table
        else:
            table_name = own_table + ', ' + link_table
            # example: 'device_sensor.SubId=device_sensor_coil.SubId'
            where = own_table+'.'+link+'='+link_table+'.'+link

        # get table from database
        table = self._get_table_data(table_name, where)

        # # delete id attribute from table
        # for element in table:
        #     del element['id']
    
        return table

    def get_device_id_data_from_dev_type(self, dev_type:str, id:int) -> dict:
        ''' get data of a special device id data from a dev type (without common stuff e.g. order code, ...) '''

        # get table of device type
        table = self.list_device_type_info(dev_type)

        # identifier
        _, _, identfier = self._get_definition_tables_linked(dev_type, level='middle')
        
        # filter id
        for row in table:
            if row[identfier] == id:
                return row

        return None

    def list_device(self, device_type=None) -> list:
        ''' return dict list of a device with all information
        with filter option device type
        '''
        # get default table
        table_name = 'device'

        # get table from database
        table = self._get_table_data(table_name)

        # sort table
        sort_table = []
        if device_type != None:
            for row in table:
                if device_type == row['DeviceType']:
                    sort_table.append(row)
        else:
            sort_table = table

        # add special device infos
        for row in sort_table:
            # get additional infos from device type table
            add_dict = self.get_device_id_data_from_dev_type(dev_type=row['DeviceType'], id=row['DeviceId'])
            # # delete id pointer
            # del add_dict['id']
            # add to row
            row.update(add_dict)

        self.logger.debug("Read library device table information for device type '{}'.".format(device_type))

        return sort_table

    def list_order_code(self, device_type=None) -> list:
        ''' return list of order codes of all devices 

        filter option device_type
        '''
        # get total device list
        device_list = self.list_device(device_type)

        # init table
        table = []
        # get order code from every device
        for device in device_list:
            table.append(device['OrderCode'])
        # return
        return table

    def edit_device(self, dev_type:str, changes:dict):
        ''' change libary content by device type (with handle different tables) '''

        # get type information of view
        type = self._get_definition_type_by_view(dev_type)

        # get input data
        id_type = changes['where_key']
        id = changes['where_value']
        key = changes['value_key']
        new_value = changes['value']

        # change at sub device
        if type == 'sub': 
            # get table and identifier
            table_name_sub, _, identfier = self._get_definition_tables_linked(dev_type, level='bottom')
            # check id type
            if id_type != identfier:
                text = "Id type is wrong. Expected value is '{}'. Real value is '{}'!".format(identfier, id_type)
                self.logger.exception(text)
                raise ValueError(text)
            # get colum names
            column_names_sub = self._get_table_column_keys(table_name_sub)
            # seperate key by tables
            if key in column_names_sub:
                self._change_table_data(table_name=table_name_sub, where_key=id_type, where_value=id, value_key=key, value=new_value)
            # raise error if key not in table
            else:
                text = "Key '{}' not in list '{}'".format(key, column_names_sub)
                self.logger.exception(text)
                raise KeyError(text)
        # in case of normal device
        elif type == 'device': 
            # get table and identifier
            table_name_common, _, identfier_common = self._get_definition_tables_linked(dev_type, level='top', pointer='top')
            table_name_device, _, identfier_device = self._get_definition_tables_linked(dev_type, level='middle', pointer='top')
            table_name_sub, _, identfier_sub = self._get_definition_tables_linked(dev_type, level='bottom', pointer='top')

            # no change neccessary
            if table_name_sub != None:
                pass # do nothing

            # check id type
            if id_type != identfier_common:
                text = "Id type is wrong. Expected value is '{}'. Real value is '{}'!".format(identfier_common, id_type)
                self.logger.exception(text)
                raise ValueError(text)            
            # get column names
            column_names_common = self._get_table_column_keys(table_name_common) 
            column_names_device = self._get_table_column_keys(table_name_device) 
            column_names_sub = self._get_table_column_keys(table_name_sub) 

            # seperate key by tables
            if key in column_names_common:
                self._change_table_data(table_name=table_name_common, where_key=id_type, where_value=id, value_key=key, value=new_value)
            # if a key of device get device key and change data at device table
            elif key in column_names_device:
                where = "{}={}".format(identfier_common,id)
                # get common data
                common_device = self._get_table_data(table_name_common, where)
                # get device id
                dev_id = common_device[0][identfier_device]
                self._change_table_data(table_name=table_name_device, where_key=identfier_device, where_value=dev_id, value_key=key, value=new_value)
            # if a key of sub device thats very special. in general here you can't change any data. this is a human readable pointer 
            elif key in column_names_sub:
                # check if human readable pointer is true
                # get table key information
                tables = self._get_definition_tables_by_view(dev_type)
                for table in tables:
                    if table['level'] == 'bottom':
                        table_key = table['key']
                        break
                # check if key matches with table key
                if table_key != key:
                    text = "Key '{}' is not the right table key '{}'!".format(key, table_key)
                    self.logger.exception(text)
                    raise Exception(text)
                # if table key is correct
                else:
                    where = "{}={}".format(identfier_common,id)
                    # get common data
                    common_device = self._get_table_data(table_name_common, where)
                    # get device id
                    dev_id = common_device[0][identfier_device]
                    # get sub data
                    where = "{}='{}'".format(key,new_value)
                    # get sub data
                    sub_device = self._get_table_data(table_name_sub, where)
                    # get new sub id
                    new_sub_id = sub_device[0][identfier_sub]
                    self._change_table_data(table_name=table_name_device, where_key=identfier_device, where_value=dev_id, value_key=identfier_sub, value=new_sub_id)
            # raise error if key not in table
            else:
                text = "Key '{}' not in list '{}'".format(key, column_names_device + column_names_common)
                self.logger.exception(text)
                raise KeyError(text)
        else:
            text = "Definition type '{}' is unsupported".format(type)
            self.logger.exception(text)
            raise ValueError(text)

    def get_device(self, order_code=None):
        ''' return device information by order code

        if device will be found in database a dict will be returned. if not a boolean false will be returned. 
        '''
        # get total device list
        device_list = self.list_device()

        # get order code from every device
        for device in device_list:
            if device['OrderCode'] == order_code:
                return device
        self.logger.info("Read library device table information for order code '{}'.".format(order_code))

        # return
        return False

    def add_default_device(self, dev_type:str):
        ''' add default libary content
        
        returns default name and id
        '''
        time_now = datetime.now()
        # get device infos and change order code
        default_device = {}
        device_name = 'Default'
        if dev_type == 'DeviceSensor':
            device_name = 'TSen' + time_now.strftime('%y%m%d%H%M%S')
            #default_device = self.get_device(order_code='Default_Sensor')
            default_device['OrderCode'] = device_name
            default_device['DeviceType'] = dev_type
        elif dev_type == 'DeviceRotor':
            device_name = 'TRot' + time_now.strftime('%y%m%d%H%M%S')
            #default_device = self.get_device(order_code='Default_Rotor')
            default_device['OrderCode'] = device_name
            default_device['DeviceType'] = dev_type
        elif dev_type == 'DeviceMultiplexer': 
            device_name = 'TMux' + time_now.strftime('%y%m%d%H%M%S')
            #default_device = self.get_device(order_code='Default_Mux')
            default_device['OrderCode'] = device_name
            default_device['DeviceType'] = dev_type
        elif dev_type == 'DeviceSensor_Coil': 
            device_name = 'TCoi' + time_now.strftime('%y%m%d%H%M%S')
            #default_device = self._get_table_data(table_name='device_sensor_coil', where="ElementType='Default_Coil'")
            #default_device = default_device[0]
            default_device['ElementType'] = device_name
        else:
            text = "Unknown device type!".format(dev_type)
            self.logger.exception(text)
            raise Exception(text)
        #pprint(default_device)
        
        # add library content
        id =  self.add_device(dev_type, default_device)
        return device_name, id

    def add_device(self, dev_type:str, new_device:dict) -> int:
        ''' add libary content by device type (with handle different tables)

        new_device don't need all fields. on unset fields this function use the default value of mysql database
        
        insert field new device into mysql tables
        - in case of a sub device new sub device will be created
        - in case of a normal device a now row to common table and a row to device specific table will be created (sub info will be checked)

        '''
        # get table information
        tables = self._get_definition_tables_by_view(dev_type)
        # get type information of view
        type = self._get_definition_type_by_view(dev_type)

        self.logger.debug("Create a new device with following data {} ".format(new_device))

        # in case of a sub view
        if type == 'sub': 
            # get table and identifier
            table_name_sub, _, _ = self._get_definition_tables_linked(dev_type, level='bottom', pointer='top')
            # add to sub table
            sub_id, new_device, _ = self._add_new_table_row(table_name_sub, new_device, raise_error=True)
            # check for too much input data
            if list(new_device.keys()) != []:
                text = "Fields '{}' not found in common, device (and sub) table!".format(list(new_device.keys()))
                self.logger.exception(text)
                raise KeyError(text)
            return sub_id
        # in case of normal device
        elif type == 'device':
            # get table and identifier
            table_name_sub, _, identifier = self._get_definition_tables_linked(dev_type, level='bottom', pointer='top')
            # has device a special sub device
            if table_name_sub != None:
                # add to sub table
                sub_id, new_device, _ = self._add_new_table_row(table_name_sub, new_device, raise_error=True, create_a_new_if_empty=False)
                # add link to device
                if dev_type == 'DeviceSensor':
                    where="{}={}".format(identifier, sub_id)
                    sub_data = self._get_table_data(table_name_sub, where)
                    new_device[identifier] = sub_data[0][identifier]

            # get table and identifier
            table_name_device, _, identifier = self._get_definition_tables_linked(dev_type, level='middle')
            # add to device table
            device_id, new_device, _ = self._add_new_table_row(table_name_device, new_device, create_a_new_if_exist=True)
            new_device[identifier] = device_id
            # get table and identifier
            table_name_common, _, _ = self._get_definition_tables_linked(dev_type, level='top')
            # add to common table
            common_id, new_device, _ = self._add_new_table_row(table_name_common, new_device, create_a_new_if_exist=True)
            # check for to much input data
            if list(new_device.keys()) != []:
                text = "Fields '{}' not found in common, device (and sub) table!".format(list(new_device.keys()))
                self.logger.exception(text)
                raise KeyError(text)
            return common_id
        else:
            text = "Definition type '{}' is unsupported".format(type)
            self.logger.exception(text)
            raise ValueError(text)

    def _add_new_table_row(self, table_name:str, new_device:dict, raise_error=False, create_a_new_if_empty=True, create_a_new_if_exist=True):
        ''' add new row if not exists

        if already exists and raise_error = True: an exception occured.
        if the new_device information for the table is empty and the create_a_new_if_empty is False a default value will be taken

        returns id (primary key) and rest of new_device, and existing flag
        '''
        # get primary key of table
        pri_key = self._get_primary_key(table_name)
        # get fields
        fields = list(new_device.keys())
        # cleanup primary key
        if pri_key[0] in fields:
            del new_device[pri_key[0]]
        # init add struct
        add_device = {}
        # get column names of specific device
        column_names = self._get_table_column_keys(table_name)
        # set up add data
        for field in fields:
            if field in column_names:
                # add
                add_device[field] = new_device[field]
                # delete from input
                del new_device[field]

        # check if exist in library
        _, id = self._check_if_libary_data_exists(table_name=table_name, data=add_device)
        # if not existing, create
        if id == None:
            # set flag
            exist = False
            # no information is set and flag is false
            if create_a_new_if_empty == False and add_device == {}:
                if table_name == 'device_sensor_coil':
                    add_device = {'ElementType':'Default'}
                # elif table_name == 'device_sensor':
                #     add_device = {'HousingType':'Default'}
                # elif table_name == 'device_rotor':
                #     add_device = {'RotorType':'Default'}
                # elif table_name == 'device_multiplexer':
                #     add_device = {'MuxDescription':'Default'}
                else:
                    text = "Table '{}' not implemted yet.".format(table_name)
                    self.logger.error(text)
                    raise ValueError(text)
                # get default value
                _, id = self._check_if_libary_data_exists(table_name=table_name, data=add_device)
                return id, new_device, exist
            # create a new one
            else:
                id = self._insert_table_data(table_name=table_name, data=add_device, auto_add=False)
                return id, new_device, exist
        # in case of existing, submit error
        else:
            # set flag
            exist = True
           # create a new one
            if create_a_new_if_exist == True:
                id = self._insert_table_data(table_name=table_name, data=add_device, auto_add=False)
                return id, new_device, exist
            else:
                # set text
                text = "Data {} at table '{}' exist already!".format(add_device, table_name)
                if raise_error:
                    self.logger.exception(text)
                    raise ValueError(text)
                else:
                    self.logger.error(text)
                    return id, new_device, exist

_mysql_lib_singelton = _mysql_lib()

# Singelton
def mysql_lib():
    return _mysql_lib_singelton

# my_lib = mysql_lib()

# my_lib._get_table_column_keys('device')
# my_lib._get_table_comments('device')
# print(my_lib._check_if_libary_data_exists('definition_type_coil', {'name':'NoCoil', 'value':0}))
# sensor_list1 = my_lib.list_device_type_info('DeviceSensor')
# pprint(sensor_list1)
# # mux_list = my_lib.list_device_type_info('DeviceMultiplexer')
# # rotor_list = my_lib.list_device_type_info('DeviceRotor')
# # dat_type_list = my_lib._get_column_data_type('device_sensor_coil')
# # device_list = my_lib.list_device()
# # device_order_code_list = my_lib.list_device_by_order_code()
# # device = my_lib.device(order_code='A0M9952085001071')

# sensor_list2 = my_lib.list_device('DeviceSensor')

# pprint(sensor_list2)
# print(sensor_list2 == sensor_list1)
# table_name = 'device_history'

# data = {'UniqueId':1, 'SerialNumber':'new_col', 'OrderCode':2, 'Test_Col':10, 'DeviceType':'coil', 'VendorId':'RohmannGmbH', 'PayloadVersion':0, 'User':'bauer', 'DateTime':'2022-01-11 16:43:31'}
# my_lib._insert_table_data(table_name, data, auto_add=True)

# my_lib.close()

# print("finished")