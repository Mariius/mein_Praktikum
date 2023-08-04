import pytest
import unittest
from ino_with_py_v2 import runIno

class TestRunIno(unittest.TestCase):
    
    
    def setUp(self):    
        self.run_file=runIno("C:/Users/Praktikant1/Documents/Arduino/test_com2/test_com2.ino","COM5", "arduino:avr:nano")

    def test_allFunctions(self):
        position = 0
        length = 16
        data=[]
        content = [0x01, 0x02, 0x8C, 0xB0, 0x57, 0x4D, 0x74, 0x67, 0x2E, 0xEE, 0x3E, 0x15, 0x42, 0xA3, 0x01, 0xCB]
        # write_memory()
        assert self.run_file.write_memory(position, content)==True
        assert self.run_file.write_memory(position, content, False)==True
        # read_memory()
        assert self.run_file.read_memory(position, length, data)==['01', '02', '8C', 'B0', '57', '4D', '74', '67', '2E', 'EE', '3E', '15', '42', 'A3', '01', 'CB']
        # clear_memory()
        assert self.run_file.clear_memory()==True
        assert self.run_file.clear_memory(False)==True
        
        # write_memory()
        with pytest.raises(Exception):
            assert self.run_file.write_memory(120, content)==True
        with pytest.raises(ValueError):
            # position value ist out of the range
            assert self.run_file.write_memory(-2, content,False)==True
        with pytest.raises(ValueError):
            assert self.run_file.write_memory(129, content,False)==True
        # read_memory()
        with pytest.raises(Exception):
            assert self.run_file.read_memory(120,32, data)==['01', '02', '8C', 'B0', '57', '4D', '74', '67', '2E', 'EE', '3E', '15', '42', 'A3', '01', 'CB']
        with pytest.raises(ValueError):
            # length value ist out of the range
            assert self.run_file.read_memory(120,-2, data)==['01', '02', '8C', 'B0', '57', '4D', '74', '67', '2E', 'EE', '3E', '15', '42', 'A3', '01', 'CB']
              
   
    

if __name__ == "__main__":
    unittest.main()
