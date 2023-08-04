import logging
import tpow.usb9097
import tpow.device

import time

# own lib
from .byte_handle import byte_list_to_bytes, swap_byte, byte_to_int, int_to_byte, byte_to_hex

def crc8(data: bytes):
    crc = 0
    for i in range(len(data)):
        byte = data[i]
        for b in range(8):
            fb_bit = (crc ^ byte) & 0x01
            if fb_bit == 0x01:
                crc = crc ^ 0x18
            crc = (crc >> 1) & 0x7f
            if fb_bit == 0x01:
                crc = crc | 0x80
            byte = byte >> 1
    return crc

def crc16(data: bytearray, init=0x0000):
    # init
    offset = 0
    length = len(data)

    if data is None or offset < 0 or offset > len(data) - 1 and offset + length > len(data):
        return 0
    #print("length=", length)
    #print(data)

    crc = init
    for i in range(length):
        crc ^= data[offset + i]
        for j in range(8):
            #print(crc)
            if ((crc & 0x1) == 1):
                #print("bb1=", crc)
                crc = int((crc / 2)) ^ 40961
                #print("bb2=", crc)
            else:
                crc = int(crc / 2)
    return crc & 0xFFFF

class one_wire_prog():
    ''' class to read and write data from a one-wire-device with DS9481R '''
    def __init__(self, com_port, run_without_device=True):
        # Setup logging concept
        self.logger = logging.getLogger('prog')
        self.logger.setLevel(logging.INFO)

        # init input
        self.com_port = com_port

        # supported families
        self.supported_families = ['DS2406', 'DS2431']

        # init
        try:
            self.bus = tpow.usb9097.USB9097(self.com_port)
            self.logger.info("Connected to DS9481R via '{}'.".format(self.com_port))
        except:
            self.logger.error("Can't connect to COM port: {}".format(self.com_port))            

        # check for connected one wire device
        if run_without_device:
            # read serial number
            serial, _ = self.read_unique_id()
            self.logger.info("Connected one wire device found with following serial number '{}'.".format(serial))
        else:
            # check for connected device
            if not self.check_if_device_is_connected():
                text = "Please connect your one wire device with the programmer!"
                self.logger.exception(text)
                raise ConnectionError(text)

    def check_if_device_is_connected(self) -> bool:
        serial, _ = self.read_unique_id()
        if serial == None:
            return False
        else:
            return True

    def read_unique_id(self):
        ''' Read one wire: unique id (serial number)
        
        return
        - in case of not connected one wire device:
         > None, None
        - in case invalid one wire device:
         > False, None
        - in case valid one wire device:
         > 1283u2193821u, 'Familyname'
         '''
        self.logger.debug("Read device serial")
        self.bus.cmd_reset()                    # 0xE3, 0xC1
        self.bus.dat_write([0x33])              # read rom
        device_address = self.bus.dat_read(8)   # little-endian (family + SN[6] + CRC)
        # conver it into byte 
        unique_id_byte = byte_list_to_bytes(device_address)
        # no device is connected
        if unique_id_byte == b'\xff\xff\xff\xff\xff\xff\xff\xff':
            return None, None
        else:
            # eval
            crc = unique_id_byte[7]
            serial = unique_id_byte[1:7]
            family = unique_id_byte[0]
            # too much devices connected?
            if crc8(unique_id_byte[0:7]) != crc:
                self.logger.error("Something went wrong with the serial number of your one wire device. CRC8 does not match! Too much devices connected?")
                return False, None
            # check family
            if family == 0x12:
                self.logger.debug("DS2046 family (OTP device) connected!")
                self.logger.info("OTP one wire device connected!")
                family = 'DS2406'
            elif family == 0x2D:
                self.logger.debug("DS2431 family connected!")
                family = 'DS2431'
            else:
                self.logger.debug("One wire family unknown connected!")
                family = 'unknown'
            unique_id_int = byte_to_int(unique_id_byte)
            # convert list of binary stings into one binary string and return
            self.logger.debug("Device serial: {} [{}]".format(unique_id_byte, unique_id_int))           
            return unique_id_int, family

    def read_data(self, start_address=0x00, block_size:int=16, block_number:int=8) -> list:
        ''' Read device data as blocks
        
        - start_address: address of first data
        - block_size: size of one block in byte
        - block_number: number of blocks

        '''
        self.logger.debug("Read Data at start adress '0x{:0>2x}' in {} block(s) with '{}' byte(s):".format(start_address, block_number, block_size))
        self.bus.cmd_reset()                    # 0xE3, 0xC1
        self.bus.dat_write([0xCC])              # skip command com

        self.bus.dat_write([0xF0])              # read memory command
        self.bus.dat_write([start_address, 0x00])     # memory address

        ret =  []
        for i in range(block_number):
            memory = self.bus.dat_read(block_size)      # little-endian
            self.logger.debug("Read Memory [0x{:0>2x}]: {}".format(start_address+i*block_size, memory))
            ret.append(memory)
        
        # return only a list in case of one block
        if block_number == 1:
            return ret[0]
        else:
            return ret

    def write_data_DS2406(self, start_address = 0x30, data = 0xAA) -> bool:
        ''' write data to ds2406 device '''
        # init error flag
        error_flag = False
        # init address
        address = start_address
        # input management in case of a singe value
        if isinstance(data, int):
            in_data = []
            in_data.append(data)
            data = in_data
        # step over data
        for write_value in data:
            self.logger.debug("\nWrite Data")
            self.bus.cmd_reset()        # 0xE3, 0xC1
            self.bus.dat_write([0xCC])  # skip command com

            self.logger.info("Write Memory [0x{:0>2x}]: 0x{:0>2x}".format(address, write_value))
            self.bus.dat_write([0x0F])                  # write memory command
            self.bus.dat_write([address, 0x00])   # memory address
            self.bus.dat_write([write_value])                  # send data

            # get crc
            crc = self.bus.dat_read(2)
            self.logger.debug("Received CRC: {}".format(crc))

            #print(byte_to_int(byte_list_to_bytes(crc)))
            #print(crc16(int_to_byte(0x0F,1)+int_to_byte(address,2)+int_to_byte(data,1), 0x0000))
            # TODO Check CRC!!!!!

            self.bus.set_mode(0xE3)          # set command mode  
            self.bus.uart.write([0xFD])      # program-pulse
            self.bus.set_mode(0xE1)          # set data mode
            response = self.bus.uart.read(1)
            #bus.clear()
            #time.sleep(1)
            read_value = self.bus.dat_read(1)
            read_value = byte_to_int(read_value[0])
            self.logger.info("Written data to [0x{:0>2x}]: {}".format(address, read_value))
            self.bus.cmd_reset()        # 0xE3, 0xC1
            
            # check
            if read_value != write_value:
                self.logger.error("Write failure at address [0x{:0>2x}]!".format(address))
                error_flag = True

            # increment address pointer
            address = address + 1

        # return error flag
        return not error_flag

    def write_data_DS2431(self, start_address = 0x30, data = 0xAA) -> bool:
        ''' write data to ds2431 device

        data: bytes or int

        The device only supports full row (8-byte) copy operations
        '''
        # input management in case of a singe value
        if isinstance(data, int):
            in_data = []
            in_data.append(data)
            data = in_data

        # size of scatchpad: 8 byte
        scratchpad_size = 8
        # calc data size
        data_size = len(data)
        # add stuff at start
        new_start_address = start_address - start_address % scratchpad_size
        start_offset = start_address - new_start_address
        new_data_size = data_size + start_offset
        # add stuff at end
        end_offset = (scratchpad_size - (new_start_address + new_data_size) % scratchpad_size) % scratchpad_size
        new_data_size = new_data_size + end_offset
        if (new_data_size % scratchpad_size) != 0:
            text = "Something went wrong by calculating DS2431 data copy stuff!"
            self.logger.exception(text)
            raise ValueError(text)
        # read existing data and covnert new data
        if start_address != new_start_address or data_size != new_data_size:
            existing_data = self.read_data(new_start_address, new_data_size, 1)
            # replace existing data with new data
            for i in range(data_size):
                if isinstance(data[i], bytes):
                    existing_data[i+start_offset] = data[i]
                else:
                    existing_data[i+start_offset] = int_to_byte(data[i], 1)
            data = byte_list_to_bytes(existing_data)
        
        # convert data
        data = bytearray(data)
        # init address
        address = new_start_address
        # init error flag
        error_flag = False
        while(1):
            # break if data is copied to scratchpad
            if len(data) == 0:
                break
            # copy data into own variable
            scratchpad_data = data[0:scratchpad_size]
            # init scratchpad start address 
            current_scratchpad_start_address = address
            # remove from data
            del data[0:scratchpad_size]
            self.logger.debug("Current scratchpad data block: {} with a size of '{}' byte(s).".format(scratchpad_data, scratchpad_size))
            self.logger.debug("Current scratchpad start address: 0x{:0>2x}".format(current_scratchpad_start_address))
            
            self.logger.debug("Write Data")
            self.bus.cmd_reset()                # 0xE3, 0xC1
            self.bus.dat_write([0xCC])          # skip command com
            self.bus.dat_write([0x0F])          # write scratchpad command
            self.bus.dat_write([current_scratchpad_start_address, 0x00]) # memory address
            # copy data to scratchpad (in size of 8 byte)
            self.bus.dat_write(scratchpad_data)  # send data
            # increment address pointer
            address = address + scratchpad_size
            # crc = self.bus.dat_read(2)                  # get crc
            # self.logger.debug("crc = {}".format(crc))
            self.bus.cmd_reset()                # 0xE3, 0xC1
            self.bus.dat_write([0xCC])          # skip command com

            self.logger.debug("Read Scratchpad")
            self.bus.dat_write([0xAA])          # read scratchpad command
            ta_es = self.bus.dat_read(3)        # get ta1, ta2 and e/s
            self.logger.debug("TA_E/S = {}".format(ta_es))
            ta1 = byte_to_int(ta_es[0])
            ta2 = byte_to_int(ta_es[1])
            if ta1 != current_scratchpad_start_address:
                self.logger.error("Invalid start address!")
            if ta2 != 0x00:
                self.logger.error("Invalid ta2!")
            es = byte_to_int(ta_es[2])
            self.logger.debug("E/S = 0x{:0>2x}".format(es))
            if bool(es & 0b00100000):
                self.logger.error("Invalid Scratchpad. PF flag is high!")
            scratch = self.bus.dat_read(scratchpad_size) # read scratchpad data and verify
            # compare scratchpad data
            self.logger.debug("Scratch = {}".format(scratch))
            if bytearray(b''.join(scratch)) != scratchpad_data:
                self.logger.error("Current scratchpad data block '{}' does not match with scratchpad data '{}'".format(scratchpad_data, bytearray(b''.join(scratch))))
                error_flag = True
            # crc = self.bus.dat_read(2)                  # get crc
            # self.logger.debug("crc = {}".format(crc))
            self.bus.cmd_reset()        # 0xE3, 0xC1
            self.bus.dat_write([0xCC])  # skip command com

            self.logger.debug("Copy Scratchpad")
            self.bus.dat_write([0x55])                      # copy scratchpad command
            self.bus.dat_write([current_scratchpad_start_address, 0x00, es])  # send ta1, ta2, es
            time.sleep(0.012)                               # wait tPROGMAX for the copy function to complete = 10ms
            copy_status = self.bus.dat_read(1)              # read copy status: 0xAA for success
            copy_status = byte_to_int(copy_status[0])  
            self.bus.cmd_reset()        # 0xE3, 0xC1
            #self.bus.dat_write([0xCC])  # skip command com
            # check copy status
            self.logger.debug("Copy status = 0x{:0>2x}".format(copy_status))
            # set error flag in case of an error
            if copy_status != 0xAA:
                error_flag = True 

            # read_dat = self.read_data(current_scratchpad_start_address, current_scratchpad_size, 1)
            # self.logger.info("{}".format(read_dat))

        # return error flag
        return not error_flag

    def close(self):
        self.logger.info("Close serial port '{}'".format(self.com_port))
        self.bus.close()
