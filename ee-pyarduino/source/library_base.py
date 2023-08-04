import mysql.connector
import mysql.connector.locales.eng.client_error
import logging

class mysql_lib_base(object):
    ''' library class

    - read data from mysql library
    - save data to mysql library
    '''

    def __init__(self, user='root', password='password', host='127.0.0.1', port='3306', database='database'):
        ''' init '''
        # Setup logging concept
        self.logger = logging.getLogger('library')
        self.logger.setLevel(logging.INFO)

        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

        self.logger.info("Open library connection to host '{}:{}' at database '{}' with user '{}'.".format(self.host, self.port, self.user, self.database))

        # connect to database 
        # see: https://workingninja.com/bad-handshake-mysql-connector-python-package
        #self.logger.info("Initialize and connect to mysql library '{}'".format(self.database))
        self.cnx = mysql.connector.connect(user=self.user, password=self.password, host=self.host, port=self.port, database=self.database, charset='utf8', use_pure=True)
        self.cursor = self.cnx.cursor()

    def close(self):
        ''' close connection'''
        self.logger.info("Close library connection '{}'.".format(self.database))
        # close
        self.cursor.close()
        self.cnx.close()

    # def _convert_to_dict(self, fetched_data):
    #     ''' convert to dictionary '''
    #     ret = {}
    #     # set over all tuples
    #     for tuple in fetched_data:
    #         ret[tuple[1]] = tuple[0].to_bytes(1,'little')
    #     return ret

    def _insert_table_data(self, table_name:str, data:dict={}, auto_add=False) -> int:
        ''' insert data of a mysql table

        if auto_add = True: if the data has a key that is not in the lib, a new column will be created
        if data = is empty the default values will be taken

        # example:
            table_name = 'device_history'
            data = {'UniqueId':1, 'SerialNumber':'sadsd', 'OrderCode':2, 'DeviceType':'coil', 'VendorId':'RohmannGmbH', 'PayloadVersion':0, 'User':'bauer', 'DateTime':'2022-01-07 16:43:31'}
            my_lib._insert_table_data(table_name, data)

        '''
        # get table fields
        table_fields = self._get_column_data_type(table_name)

        # search data keys in existing table fields. add data if add-flag is true
        for data_key in data.keys():
            found = False
            for table_field in table_fields:
                if data_key == table_field['Field']:
                    found = True
            if not found:
                self.logger.info("Key '{}' not found in fields of table '{}'.".format(data_key, table_name))
                # add a new field if field does not exist
                if auto_add:
                    if isinstance(data[data_key], int):
                        data_type = 'int(10)'
                    elif isinstance(data[data_key], float):
                        data_type = 'float'
                    elif isinstance(data[data_key], str):
                        data_type = "char(50) NULL DEFAULT NULL COLLATE 'utf8_general_ci'"
                    else:
                        text = "Could not add data '{}' to table '{}'. To add data type '{}' is not implemented!".format(data_key, table_name, type(data[data_key]))
                        self.logger.exception(text)
                        raise KeyError(text)
                    # add column
                    # query = "ALTER TABLE {} ADD COLUMN IF NOT EXISTS {} {}".format(table_name, data_key, data_type)
                    query = "ALTER TABLE {} ADD {} {}".format(table_name, data_key, data_type)
                    self.cursor.execute(query)
                    self.logger.info("Add field '{}' to table '{}' with data type '{}'.".format(data_key, table_name, data_type))
                else:
                    text = "Could not add data '{}' to table '{}'. Please use option 'auto_add' or add this key by hand.".format(data_key, table_name)
                    self.logger.exception(text)
                    raise KeyError(text)

        # generate query info
        val_string = '('+'%s, '*(len(data)-1) + '%s)'
        key_string = ''
        val = []
        for key in data.keys():
            if key_string == '':
                key_string = key
            else:
                key_string = key_string + ', ' + key
            val.append(str(data[key]))
        
        # generate query with values
        if key_string != '' and val_string != '':
            query = ("INSERT INTO {} ({}) VALUES {}".format(table_name, key_string, val_string))
        # generate a query with default values
        else:
            query = ("INSERT INTO {} () VALUES ()".format(table_name))
    
        # update data
        self.cursor.execute(query, val)

        # commit data
        self.cnx.commit()

        # get id 
        id = self.cursor.lastrowid

        self.logger.info("Record {} inserted into '{}' at id '{}'.".format(data, table_name, id))

        return id

    def _change_table_data(self, table_name:str, where_key:str, where_value, value_key:str, value):
        ''' change value in a mysql table
        '''
        # generate query
        if (isinstance(value, int) or isinstance(value, float)) and (isinstance(where_value, int) or isinstance(where_value, float)):
            query = ("UPDATE {} SET {} = {} WHERE {} = {}".format(table_name, value_key, str(value), where_key, str(where_value)))
        elif (isinstance(value, int) or isinstance(value, float)) and isinstance(where_value, str):
            query = ("UPDATE {} SET {} = {} WHERE {} = '{}'".format(table_name, value_key, str(value), where_key, str(where_value)))
        elif isinstance(value, str) and (isinstance(where_value, int) or isinstance(where_value, float)):
            query = ("UPDATE {} SET {} = '{}' WHERE {} ='{}'".format(table_name, value_key, str(value), where_key, str(where_value)))
        elif isinstance(value, str) and isinstance(where_value, str):
            query = ("UPDATE {} SET {} = '{}' WHERE {} = '{}'".format(table_name, value_key, str(value), where_key, str(where_value)))
        else:
            text = "Not handled yet."
            self.logger.exception(text)
            raise Exception(text)

        # update data
        self.cursor.execute(query)

        # commit data
        self.cnx.commit()

        self.logger.debug("Changed value in table {}.".format(table_name))

    def _get_primary_key(self, table_name:str) -> list:
        ''' get primary keys as column name '''
        query = "SELECT k.column_name FROM information_schema.key_column_usage k  WHERE k.table_name = '{}' AND k.constraint_name LIKE 'PRIMARY'".format(table_name)
        self.cursor.execute(query)
        ans = self.cursor.fetchall()
        # handle return list
        ret = []
        for elem in ans:
            ret.append(elem[0])
        return ret

    def _get_table_data(self, table_name:str, where:str='') -> list:
        ''' return a list of dicts from mysql table
        
        Example:
            > _get_table_data('user', "name='" + change_level_user + "'")
        '''
        if table_name == None:
            return None

        if where == '':
            # generate query
            query = ("SELECT * FROM {}".format(table_name))
            # get data
            self.cursor.execute(query)
        elif where.split('=')[1].isdigit():
            # generate query
            query = ("SELECT * FROM {} WHERE {} = %s".format(table_name, where.split('=')[0]))
            # get data
            self.cursor.execute(query, (where.split('=')[1],))
        else:
            # generate query
            query = ("SELECT * FROM {} WHERE {}".format(table_name, where))
            # get data
            self.cursor.execute(query)

        # get column names
        column_names = self.cursor.column_names
        # get data as tuples
        rows = self.cursor.fetchall()

        # generate a empty list
        ret = []
        for i, row in enumerate(rows):
            # generate a empty dict (fill list)
            ret.append({})
            for j, column_name in enumerate(column_names):
                ret[i][column_name] = row[j]
        
        self.logger.debug("Get table data of '{}'".format(table_name))
    
        return ret

    def _get_table_column_keys_and_comments(self, table_name:str) -> list:
        ''' return a list of colum names and the comment of mysql table   '''
        query = "SHOW FULL COLUMNS FROM {}".format(table_name)
        # get data
        self.cursor.execute(query)
        # get data as tuples
        infos = self.cursor.fetchall()
        # generate a empty list
        ret = []
        for info in infos:
            ret.append((info[0], info[-1]))
        return ret

    def _get_table_column_keys(self, table_name:str, where:str='') -> list:
        ''' return a list of column keys from mysql table '''
        if table_name == None:
            return None
        # get table
        table = self._get_table_data(table_name, where)
        # return keys
        return list(table[0].keys())

    def _get_table_column_data(self, table_name:str, column:str, where:str='') -> list:
        ''' return a list of column data from mysql table '''
        if table_name == None:
            return None

        table = self._get_table_data(table_name, where)

        # check if column exist in keys
        if column in table[0].keys():
            # create a empty list
            ret = []
            for row in table:
                ret.append(row[column])
            return ret
        else: 
            text = "No column '{}' in table '{}'!".format(column, table_name)
            self.logger.exception(text)
            raise ValueError(text)   

    def _get_column_data_type(self, table) -> list:
        ''' return a list of dicts from mysql table '''
        # generate query
        query = ("SHOW FIELDS FROM {}".format(table))
        # get data
        self.cursor.execute(query)

        # get column names
        column_names = self.cursor.column_names
        # get data as tuples
        rows = self.cursor.fetchall()

        # generate a empty list
        ret = []
        for i, row in enumerate(rows):
            # generate a empty dict (fill list)
            ret.append({})
            for j, column_name in enumerate(column_names):
                ret[i][column_name] = row[j]
            
        return ret

    def _delete_table_data(self, table_name:str, where:str=''):
        ''' delete data from mysql table '''
        if where == '':
            # generate query
            query = ("DELETE FROM {}".format(table_name))
        else:
            # generate query
            query = ("DELETE FROM {} WHERE {}".format(table_name, where))
        # delete data
        self.cursor.execute(query)
        # commit
        self.cnx.commit()
        
        self.logger.debug("Delete table data of '{}'".format(table_name))

    def _check_if_libary_data_exists(self, table_name:str, data:dict):
        ''' check if libary content exists

        return the primary key and the value of it
        if nothing to find: a None-Tye will be returned
        '''

        # if no filter is set, none type will be returned
        if data == {}:
            return None, None
        
        where = ''
        for key in list(data.keys()):
            if isinstance(data[key], int):
                where = where + key + '=' + str(data[key]) + " and "
            elif isinstance(data[key], float):
                where = where + key + "=" + str(data[key]) + " and "
            elif isinstance(data[key], str):
                where = where + key + "='" + data[key] + "' and "
            else:
                text = "Unknown datatype of value '{}'!".format(data[key])
                self.logger.exception(text)
                raise TypeError(text)   
        # cut tail
        where = where[:-5]
        #print(where)
        # get data
        table_data = self._get_table_data(table_name, where)
        # found nothing
        if len(table_data) == 0:
            text = "Nothing found table at '{}' data where {}".format(table_name, where)
            self.logger.debug(text)
            return None, None
        # found too much data
        if len(table_data) > 1:
            text = "More than one positions found table at '{}' data where {}. Hint: only one position is returned!".format(table_name, where)
            self.logger.warning(text)

        columns = list(table_data[0].keys())

        # get primary key
        pri_key = self._get_primary_key(table_name)
        # return value of primary key
        if pri_key[0] in columns:
            return pri_key[0], table_data[0][pri_key[0]]
        return pri_key[0], None

