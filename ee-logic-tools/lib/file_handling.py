import os
import stat
import shutil
import json
import tarfile
#import yaml
#import xmltodict
import glob
import hashlib
import re
from typing import Union

def check_if_folder_exist(folder):
    return os.path.isdir(folder)

def check_if_file_exist(file):
    return os.path.isfile(file)

def create_bzip2_file(path, filename):
    # create compressed file in write mode
    compessed_file = tarfile.open(filename, "w:bz2")
    # add files in path folder
    for root, dirs, files in os.walk(path):
        for f in files:
            compessed_file.add(os.path.join(root, f))
    # close file
    compessed_file.close()

def create_text_file(content, filename):
    with open(filename, 'w') as f:
        if isinstance(content,str):
            f.write(content)
        else:
            for item in content:
                f.write(item + '\n')

def get_filename(path, pattern:Union[str,list]) -> str:
    ''' check if file exist and return the newest version of file
    
    hierarchy: default = None, or a list of fileendings (first value is important)

    Arguments:
        path: path name of folder
        name_pattern: r'motherboard2_(\d+v\d+).svf'

    '''
    # init filelist
    file_list = []
    if isinstance(pattern, str):
        pattern = [pattern]
    for item_pattern in pattern:
        # int regex
        regex = re.compile(item_pattern)

        # step over all files and find files
        for root, dirs, files in os.walk(path):
            for file in files:
                if regex.match(file):
                    file_list.append(file)
        
        # if nothing found, try to change the pattern
        if len(file_list) == 0:
            pos = item_pattern.find('(\\d+v\\d+)')
            if pos != -1:
                # delete first '\d+' from  '(\\d+v\\d+)'
                new_item_pattern = item_pattern[:pos+1] + item_pattern[pos+4:]
                #print(new_item_pattern)
                # int regex
                regex = re.compile(new_item_pattern)
                # step over all files and find files
                for root, dirs, files in os.walk(path):
                    for file in files:
                        if regex.match(file):
                            file_list.append(file)
    
    # raise if nothing found
    if len(file_list) == 0:
        print("No filename found for pattern '{}' at path '{}'!".format(pattern, path))
        return None
    # in case of one file
    elif len(file_list) == 1:
        return file_list[0]
    # try to sort for newest version
    else:
        # analyse hierarchy
        hierarchy = None
        search_hierarchy = re.findall(r'([a-z]{3}\|[a-z]{3})', item_pattern)
        if len(search_hierarchy) == 0:
            pass
        elif len(search_hierarchy) == 1:
            hierarchy = search_hierarchy[0].split('|')    # create a list of extensions: first has the highest hierarchy
        else:
            raise ValueError("Unhandled hiercharcy problem")
        #print(hierarchy)
        #print(file_list)
        # init return values
        ret_file = ''
        ret_version = ''
        hier_index = 999
        #print("retfile: '{}'".format(ret_file))
        #print("ret_version: '{}'".format(ret_version))
        #print("hier_index: '{}'".format(hier_index))
        # go over file list
        for file in file_list:
            #print("file: '{}'".format(file))
            # get verion of current filename
            version = get_version_from_filename(file, with_build_info=True)
            #print("version: '{}'".format(version))
            #print("compare: '{}'".format(version >= ret_version))
            # is version 
            if version >= ret_version:
                # in case of no hierarchy, take this one
                if hierarchy == None:
                    ret_file = file
                    ret_version = version
                # in the other case, analyze the extension
                else:
                    # get extension
                    _, extension = os.path.splitext(file)
                    # cut the leading dot
                    extension = extension[1:]
                    #print(extension)
                    # is extension in hierarchy list
                    if extension in hierarchy:
                        #print(hierarchy.index(extension))
                        # is current version is larger than the last one, replace file
                        if version > ret_version:
                            #print('replace')
                            #print(file)
                            ret_file = file
                            ret_version = version
                            hier_index = hierarchy.index(extension)    
                        # if current version is equal and current index is smaller than the last one, replace file
                        elif hierarchy.index(extension) <= hier_index:
                            #print('replace')
                            #print(file)
                            ret_file = file
                            ret_version = version
                            hier_index = hierarchy.index(extension)
                    # is extension not in hierarchy list
                    else:
                        # and the index is the default index
                        if hier_index == 999:
                            # update file
                            ret_file = file
                            ret_version = version
                    #print("retfile: '{}'".format(ret_file))
                    #print("ret_version: '{}'".format(ret_version))
                    #print("hier_index: '{}'".format(hier_index))
        
        return ret_file

def copy_folder_content(source, dest):
    """Copy a directory structure overwriting existing files

    shutil.copytree(src_dir, dest_dir, dirs_exist_ok=True) works only with python 3.8+
    """
    print("Copy (overwrite) content from source '{}' to destination '{}'.".format(source, dest))

    for root, dirs, files in os.walk(source):
        if not os.path.isdir(root):
            os.makedirs(root)

        for file in files:
            rel_path = root.replace(source, '').lstrip(os.sep)
            dest_path = os.path.join(dest, rel_path)

            if not os.path.isdir(dest_path):
                os.makedirs(dest_path)

            shutil.copyfile(os.path.join(root, file), os.path.join(dest_path, file))

def create_folder_if_not_exist(path):
    if not os.path.isdir(path):#os.path.isdir(os.path.dirname(path)):
        os.makedirs(path)

def delete_folder(folder_name:str):
    def del_rw(action, name, exc):
        os.chmod(name, stat.S_IWRITE)
        os.remove(name)
    if os.path.isdir(folder_name):
        shutil.rmtree(folder_name, ignore_errors=False, onerror=del_rw)
        print("Folder '{}' removed from local disk.".format(folder_name))
        return True
    else:
        return False

def delete_content(folder_name:str):
    for filename in os.listdir(folder_name):
        file_path = os.path.join(folder_name, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def delete_file(file_name:str, folder_name=None, interactive:bool=True):
    ''' delete file in folder

    Example:
        >>> delete_file('*.txt', interactive=False)
        File 'test.txt' removed.,
    '''
    files = get_file_list(folder_name=folder_name, file_name=file_name)
    if files == None:
        return False

    #print(files)

    # iterate over files    
    for file in files:
        delete = True
        # if interactice ask user
        if interactive:
            ans = input("Do you want to delete file '{}'? Yes [default] or No:".format(file))
            if ans in ['y', 'Y', 'yes', 'YES', 'Yes', '']:
                delete = True
            elif ans in ['n', 'N', 'no', 'NO', 'No']:
                delete = False
            else:
                delete = False
                print("Unkown input!")
        if delete:
            os.remove(file)
            print("File '{}' removed from local disk.".format(file))
    return True

def get_file_list(folder_name=None, file_name=None):
    ''' get file list of folder

    Example:
        >>> get_file_list(folder_name='download', file_name='*.txt')
        ['C:\\repository_git\\action-package-deploy\\download\\test-pkg1-20211008083110.txt']
    '''
    # get folder
    if folder_name == None:
        folder_name = os.getcwd()
    else:
        if os.path.isdir(folder_name):
            folder_name = os.path.abspath(folder_name)
        else:
            print("Folder '{}' does not exist!".format(folder_name))
            return None

    # if no filename is set, take all files
    if file_name==None:
        file_name='*'

    # get files with regex option
    files = glob.glob(os.path.join(folder_name, file_name))

    return files

# def read_xml_file(file_name:str='', raise_error:bool=True) -> dict:
#     ''' read a xml file '''

#     # handle if file not exists
#     if not os.path.isfile(file_name):
#         if raise_error:
#             print("ERROR: Xml file '{}' does not exist!".format(file_name))
#         return {}

#     # Read XML file
#     with open(file_name, 'r') as stream:
#         data = xmltodict.parse(stream.read())
    
#     return data['xml']

# def read_yaml_file(file_name:str='', raise_error:bool=True) -> dict:
#     ''' read a yaml file '''

#     # handle if file not exists
#     if not os.path.isfile(file_name):
#         if raise_error:
#             print("ERROR: Yaml file '{}' does not exist!".format(file_name))
#         return {}

#     # Read YAML file
#     with open(file_name, 'r') as stream:
#         data = yaml.safe_load(stream)
    
#     return data

def read_json_file(file_name:str='', raise_error:bool=True) -> dict:
    ''' read a json file '''

    # handle if file not exists
    if not os.path.isfile(file_name):
        if raise_error:
            print("ERROR: JSON file '{}' does not exist!".format(file_name))
        return {}

    # Read JSON file
    with open(file_name, 'r') as stream:
        data = json.load(stream)
    
    return data

def get_file_hash(file_name:str='') -> str:
    with open(file_name,"rb") as f:
        bytes = f.read() # read entire file as bytes
        readable_hash = hashlib.sha256(bytes).hexdigest()
    return readable_hash

def get_file_size(file_name:str=''):
    file = open(file_name, 'rb')
    file.seek(0,2) # move the cursor to the end of the file
    size = file.tell()
    return size
    
def read_text_file(file_name:str='', raise_error:bool=True) -> dict:
    ''' read a text file '''

    # handle if file not exists
    if not os.path.isfile(file_name):
        if raise_error:
            print("ERROR: Text file '{}' does not exist!".format(file_name))
        return {}

    # Read text file
    with open(file_name, 'r', encoding='utf-8') as stream:
        data = stream.read()
    
    return data

def read_binary_file(file_name:str='', raise_error:bool=True) -> dict:
    ''' read a binary file '''

    # handle if file not exists
    if not os.path.isfile(file_name):
        if raise_error:
            print("ERROR: Text binary '{}' does not exist!".format(file_name))
        return {}

    # Read text file
    with open(file_name, 'rb') as stream:
        data = stream.read()
    
    return data

def get_version_from_filename(filename: str, with_build_info:bool=False) -> str:
    ''' get version from filename
    '''
    # input handling
    if not isinstance(filename, str):
        raise ValueError("Filename '{}' is not a string value!".format(filename))
    # reduce to filename without extension
    fileName, ext = os.path.splitext(filename)
    fileName = os.path.basename(fileName)
    # # try to get a version like this: _1v03.2
    # logic_version = re.findall(r'(_\d+v\d+\.\d+)',fileName)
    # #print(logic_version)
    # if len(logic_version) == 1:
    #     versionSeperateByVDot = logic_version[-1][1:].replace('v', ' ').replace('.', ' ').split()
    #     major = versionSeperateByVDot[0].lstrip('0').zfill(1)
    #     minor = versionSeperateByVDot[1].lstrip('0').zfill(1)
    #     patch = versionSeperateByVDot[2].lstrip('0').zfill(1)
    #     return major + '.' + minor + '.' + patch
    # try to get a version like this: _1v03
    logic_version = re.findall(r'(_\d+v\d+)',fileName)
    #print(logic_version)
    if len(logic_version) == 1:
        versionSeperateByV = logic_version[-1][1:].split('v')
        major = versionSeperateByV[0].lstrip('0').zfill(1)
        minor = versionSeperateByV[1].lstrip('0').zfill(1)
        return major + '.' + minor + '.0'
    else:
        # try to get a version like this: _v03
        logic_version = re.findall(r'(_v\d+)',fileName)
        #print(logic_version)
        if len(logic_version) == 1:
            versionSeperateByV = logic_version[-1][1:].split('v')
            major = versionSeperateByV[0].lstrip('0').zfill(1)
            minor = versionSeperateByV[1].lstrip('0').zfill(1)
            return major + '.' + minor + '.0'
        else:
            # try to get version like this: -2.1.15R-320
            # seperate by dots
            fileNameSeperateByDot = fileName.split('.')
            #print(fileNameSeperateByDot)
            # in case of major minor micro
            if len(fileNameSeperateByDot) == 3:
                major = fileNameSeperateByDot[0].split('-')[-1]
                minor = fileNameSeperateByDot[1]
                if with_build_info:
                    patch = fileNameSeperateByDot[2]
                else:
                    patch = fileNameSeperateByDot[2].split('-')[0]
                    # if patch ends with R or D, cut it
                    if patch[-1] == 'R' or patch[-1] == 'D':
                        patch = patch[0:-1]
                return major + '.' + minor + '.' + patch
            else:
                print("WARNING: Can't extract version information from filename '{}'!".format(filename, ))
                return None

if __name__ == "__main__":
    raise Exception('This python file is not for running itself. Please include this file into another!')
