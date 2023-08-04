import os
import subprocess
from sys import stderr

# own imports
from lib.file_handling import get_file_list, read_text_file
from xml.etree.ElementTree import parse

#############
# Functions #
#############

def run_command(command, work_dir=None):
    ''' run a command or more than one commands with subprocess
    return numerr, stdout, stderr'''
    process = subprocess.Popen(command, shell=True, cwd=work_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    outLines = stdout.decode('utf-8').split('\n')
    errLines = stderr.decode('utf-8').split('\n')
    retNum = process.returncode
    return retNum, outLines, errLines 

def edit_command(pre:str, main:str, items:dict, quotes:bool=False) -> str:
    ''' edit two commands and a lots of items to get a command call 
    
    if quotes set: add quotes around attribute of key
    '''
    call = pre + ' && ' + main
    for key in items.keys():
        call = call + ' ' + key
        if isinstance(items[key], list):
            for i in range(len(items[key])):
                if quotes:
                    call = call + ' "' + items[key][i] + '"'
                else:
                    call = call + ' ' + items[key][i]
        else:
            if quotes:
                call = call + ' "' + items[key] + '"'
            else:
                call = call + ' ' + items[key]
    return call

####################
# Init directories #
####################

# working directory
dir_work = os.path.join(os.path.dirname(__file__), os.path.pardir) # save parent dir: 'C:/repository_git/ee-maxwell-io-rs485-t55'
# target directory
dir_target = os.path.join(dir_work, 'outflow')
# system directory
dir_sys = os.path.join('C://', 'Efinity', '2022.2')
# python scripts directory
dir_py = os.path.join(dir_sys, 'pgm', 'bin', 'efx_pgm')
# version file
file_ver = os.path.join(dir_work, 'sources', 'version.svh')
# changelog file
file_change = os.path.join(dir_work, 'CHANGELOG.md')

# function: setup
func_start = 'setup.bat'
# function: generator
func_gen = 'efx_pgm'
# function: python
func_py = 'python3'

########################
# Parse version.h File #
########################
version_text = read_text_file(file_ver)
for text_item in version_text.split('\n'):
    if text_item.find("`define cnst_major_version") != -1:
        major = text_item.split(' ')[-1].split("'d")[-1]
    if text_item.find("`define cnst_minor_version") != -1:
        minor = text_item.split(' ')[-1].split("'d")[-1]
    if text_item.find("`define cnst_build_number") != -1:
        build = text_item.split(' ')[-1].split("'d")[-1]
print("Found version {}.{}.0-{} at version.h".format(major, minor, build))

############################
# Parse XML (Project) File #
############################

# get file lost
project_file_list = get_file_list(dir_work, '*.xml')
# get peri file list
peri_file_list = get_file_list(dir_work, '*.peri.xml')
# remove items of peri file list in project file list
for peri_file in peri_file_list:
    project_file_list.remove(peri_file)
if len(project_file_list) > 1:
    raise Exception("Too much files found as project file!\{}".format(project_file_list))
# get filename
project_file_name = project_file_list[0]

#project_file_content = read_xml_file(project_file_name)

tree = parse(project_file_name)
root = tree.getroot()
# project
str_project = root.attrib['name'] # e.g io-rs485-t55
# family & device
dev_info = root.find('{http://www.efinixinc.com/enf_proj}device_info')
dev_info_family = dev_info.find('{http://www.efinixinc.com/enf_proj}family')
str_family = dev_info_family.attrib['name'] # e.g Trion
dev_info_device = dev_info.find('{http://www.efinixinc.com/enf_proj}device')
str_device = dev_info_device.attrib['name'] # e.g T55F324
# replace '-' to '_'
str_project_out = str_project.replace('-','_')

str_version = '_{}v{}'.format(major, str.zfill(minor,2))

#############################
# Init Generate Bit File(s) #
#############################

# prepare items
items = {
    '--source': os.path.join(dir_work, 'efinity', 'place_and_route', str_project+'.lbf'), # 'C:/repository_git/ee-maxwell-io-rs485-t55/efinity/place_and_route/io-rs485-t55.lbf'
    '--dest': os.path.join(dir_target, str_project_out+str_version+'_1.hex'), # 'C:/repository_git/ee-maxwell-io-rs485-t55/outflow/io-rs485-t55.hex' 
    '--device': str_device, # 'T55F324'
    '--family': str_family, # 'Trion'
    '--periph': os.path.join(dir_target, str_project+'.lpf'), # 'C:/repository_git/ee-maxwell-io-rs485-t55/outflow/io-rs485-t55.lpf'
    '--interface_designer_settings': os.path.join(dir_target, str_project+'_or.ini'), # 'C:/repository_git/ee-maxwell-io-rs485-t55/outflow/io-rs485-t55_or.ini'
    '--enable_external_master_clock': 'off', # 'off'
    '--oscillator_clock_divider': 'DIV8', # DIV8'
    '--active_capture_clk_edge': 'posedge', # 'posedge'
    '--spi_low_power_mode': 'on', # 'on'
    '--io_weak_pullup': 'on', # 'on'
    '--enable_roms': 'smart', # 'smart'
    '--mode': 'active', # 'active'
    '--width': '1', # '1'
    '--release_tri_then_reset': 'on' # 'on'
}

# init call with x1, like:
# C:/Efinity/2022.2/bin/efx_pgm --source "C:/repository_git/ee-maxwell-io-rs485-t55/efinity/place_and_route/io-rs485-t55.lbf" --dest "C:/repository_git/ee-maxwell-io-rs485-t55/outflow/io-rs485-t55.hex" --device "T55F324" --family "Trion" --periph "C:/repository_git/ee-maxwell-io-rs485-t55/outflow/io-rs485-t55.lpf" --interface_designer_settings "C:/repository_git/ee-maxwell-io-rs485-t55/outflow/io-rs485-t55_or.ini" --enable_external_master_clock "off" --oscillator_clock_divider "DIV8" --active_capture_clk_edge "posedge" --spi_low_power_mode "on" --io_weak_pullup "on" --enable_roms "smart" --mode "active" --width "1" --release_tri_then_reset "on"
# C:/Efinity/2022.2/bin/efx_pgm --source "C:/repository_git/ee-maxwell-io-rs485-t55/efinity/place_and_route/io-rs485-t55.lbf" --dest "C:/repository_git/ee-maxwell-io-rs485-t55/outflow/io-rs485-t55.hex" --device "T55F324" --family "Trion" --periph "C:/repository_git/ee-maxwell-io-rs485-t55/outflow/io-rs485-t55.lpf" --interface_designer_settings "C:/repository_git/ee-maxwell-io-rs485-t55/outflow/io-rs485-t55_or.ini" --enable_external_master_clock "off" --oscillator_clock_divider "DIV8" --active_capture_clk_edge "posedge" --spi_low_power_mode "on" --io_weak_pullup "on" --enable_roms "smart" --mode "active" --width "4" --release_tri_then_reset "on"
call_x1 = edit_command(func_start, func_gen, items, quotes=True)

# init call with x4
# edit width and destination
items['--width'] = '4'
items['--dest'] = os.path.join(dir_work, 'outflow', str_project_out+str_version+'_4.hex') # 'C:/repository_git/ee-maxwell-io-rs485-t55/outflow/io-rs485-t55.hex' 
call_x4 = edit_command(func_start, func_gen, items, quotes=True)

############################
# Run Generate Bit File(s) #
############################

# x1
retNum, outLines, errLines = run_command(call_x1, work_dir=os.path.join(dir_sys, 'bin'))
# print 
for line in outLines:
    print(line)

# x4
retNum, outLines, errLines = run_command(call_x4, work_dir=os.path.join(dir_sys, 'bin'))
# print
for line in outLines:
    print(line)


#############################
# Init Generate SVF File(s) #
#############################
print('Start generating svf files')

# prepare items
items = {
    '--freq': '10000000',
    '--sdr_size': '500000', 
    '--hdr_length': '0',
    '--hir_length': '0',
    '--tdr_length': '1',
    '--tir_length': '10',
    'hex_to_svf': [os.path.join(dir_target, str_project_out+str_version+'_1.hex'), os.path.join(dir_target, str_project_out+str_version+'.ftdi.svf')]
}

# init call ftdi
call_ftdi = edit_command(func_start, func_py + ' ' + os.path.join(dir_py, 'export_bitstream.py'), items, quotes=False)

# prepare items
items = {
    '--freq': '12500000',
    '--sdr_size': '3000', 
    '--hdr_length': '0',
    '--hir_length': '0',
    '--tdr_length': '0',
    '--tir_length': '0',
    'hex_to_svf': [os.path.join(dir_target, str_project_out+str_version+'_1.hex'), os.path.join(dir_target, str_project_out+str_version+'.v6jtag.svf')]
}

# init call v6jtag
call_v6jtag = edit_command(func_start, func_py + ' ' + os.path.join(dir_py, 'export_bitstream.py'), items, quotes=False)

############################
# Run Generate SVF File(s) #
############################

# ftdi
retNum, outLines, errLines = run_command(call_ftdi, work_dir=os.path.join(dir_sys, 'bin'))
# print 
for line in outLines:
    print(line)

# v6jtag
retNum, outLines, errLines = run_command(call_v6jtag, work_dir=os.path.join(dir_sys, 'bin'))
# print
for line in outLines:
    print(line)

print('finished')