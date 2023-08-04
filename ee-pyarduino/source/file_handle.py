import os
import json
import shutil
import logging

logger = logging.getLogger('file')
logger.setLevel(logging.INFO)

def create_folder_if_not_exist(path):
    if not os.path.isdir(path):#os.path.isdir(os.path.dirname(path)):
        os.makedirs(path)

def remove_files_from_folder(path:str, except_files):
    ''' delete files in folder '''
    if not os.path.isdir(path):
        return False
    else:
        file_list = os.listdir(path)
        # remove excepted files from list
        for rm_file in except_files:
            if rm_file in file_list:
                file_list.remove(rm_file)
        # delete files
        for filename in file_list:
            filepath = os.path.join(path, filename)
            try:
                shutil.rmtree(filepath)
            except OSError:
                os.remove(filepath)
        return True

def read_text_file(file_path:str):
    ''' read text file '''
    file = open(file_path, 'r')
    data = file.read()
    # closing file
    file.close()
    return data

def read_binary_file(file_path:str):
    ''' read binary file '''
    file = open(file_path, 'rb')
    data = file.read()
    # closing file
    file.close()
    return data

def read_json_file(file_path:str):
    ''' read json file '''    
    # opening json file
    file = open(file_path, "r")
    # returns json object as
    # a dictionary
    data = json.loads(file.read())
    # closing file
    file.close()
    return data

def write_json_file(file_path:str, data:dict):
    ''' write json file ''' 
    with open(file_path, 'w') as fout:
        json_dumps_str = json.dumps(data, indent=4)
        print(json_dumps_str, file=fout)

def write_binary_file(file_path:str, data:bytes):
    ''' write binary file ''' 
    file = open(file_path, 'wb')
    file.write(data)
    file.close()

