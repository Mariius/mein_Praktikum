import pytest
import unittest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from ino_with_py_v2 import runIno
from oneWireTool.one_wire_tool import one_wire_tool
from source.one_wire_prog import one_wire_prog


class TestRunIno(unittest.TestCase):
    
    
    def setUp(self):    
        # self.run_file=runIno("test_com2/test_com2.ino","/dev/ttyUSB0", "arduino:avr:nano")
        self.run_file=runIno("test_com2/test_com2.ino","COM5", "arduino:avr:nano")
        self.run_file.compile_and_upload()
        self.one_wire_bus=one_wire_prog("COM3")

    def ret_read_data(self,data:list):
        d=[]
        for item in data:
            d.append(int.from_bytes(item))
        return d
    
    def test_allFunctions(self):
        position = 0
        length = 16
        data=[]
        content = [0x01, 0x02, 0x8C, 0xB0, 0x57, 0x4D, 0x74, 0x67, 0x2E, 0xEE, 0x3E, 0x15, 0x42, 0xA3, 0x01, 0xCB]
       
        # write_memory() when check==True        
        assert self.run_file.write_memory(position, content)==True
        
        # write_memory() when check==False
        assert self.run_file.write_memory(position, content, False)==True
        
        # read_memory()
        assert self.run_file.read_memory(position, length, data)==content
        
        # clear_memory() when check==True
        # assert self.run_file.clear_memory()==True
        
        # clear_memory() when check==False
        # assert self.run_file.clear_memory(False)==True
        
        # read_data from test one_wire_tool
        
        dat=self.one_wire_bus.read_data(0, 16, 1)
        assert self.ret_read_data(dat)==content
        
        # write_memory() when position + length >128 -->Exception
        with pytest.raises(Exception):
            assert self.run_file.write_memory(120, content)==True
            
        # write_memory() when position (-2) value ist out of the range --> ValueError
        with pytest.raises(ValueError):
            assert self.run_file.write_memory(-2, content,False)==True
            
        # write_memory() when position (129) value ist out of the range --> ValueError
        with pytest.raises(ValueError):
            assert self.run_file.write_memory(129, content,False)==True
            
        # read_memory()  when position + length >128 -->Exception
        with pytest.raises(Exception):
            assert self.run_file.read_memory(120,32, data)== content
            
        # write_memory() when position (-2) value ist out of the range --> ValueError
        with pytest.raises(ValueError):
            assert self.run_file.read_memory(120,-2, data)==content
        
        
              


if __name__ == "__main__":
    unittest.main()
