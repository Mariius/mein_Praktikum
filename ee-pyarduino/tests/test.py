import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from source.one_wire_prog import one_wire_prog

tt=one_wire_prog("COM3")

print(tt.read_data(0,16,1))
def test_read_data(data:list):
    d=[]
    for item in data:
        d.append(int.from_bytes(item))
    return d


bla = tt.read_data(0,16,1)
print(test_read_data(bla))
# for item in bla[0]:
#     print(int.from_bytes(item))