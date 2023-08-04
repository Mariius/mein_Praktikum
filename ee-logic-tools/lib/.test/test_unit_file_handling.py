import unittest

import sys
import os
from pathlib import Path

# >> add folders to syspath
sys.path.insert(0, str(Path(Path(__file__).parent, "..")))
# << add folders to syspath

# own imports
from file_handling import get_version_from_filename, get_filename, delete_file

class TestFileHandlingDefault(unittest.TestCase):
    test_list = [   
                    {'step': 1, 'filelist': ['a6_32v04.ftdi.svf'], 'pattern':r'a6_(\d+v\d+).(ftdi|v6jtag).svf', 'chain_type': None,
                        'expected': {'filename':'a6_32v04.ftdi.svf', 'version':'32.4.0', 'build':False, 'verify':'pass'}},
                    {'step': 2, 'filelist': ['a6_32v04.v6jtag.svf'], 'pattern':r'a6_(\d+v\d+).(ftdi|v6jtag).svf', 'chain_type': None,
                        'expected': {'filename':'a6_32v04.v6jtag.svf', 'version':'32.4.0', 'build':False, 'verify':'pass'}},
                    {'step': 3, 'filelist': ['campbell_backplane_c5a4_cpld_v01.svf'], 'pattern':r'campbell_backplane_c5a4_cpld_(\d+v\d+).svf', 'chain_type': None,
                        'expected': {'filename':'campbell_backplane_c5a4_cpld_v01.svf', 'version':'0.1.0', 'build':False, 'verify':'pass'}},
                    {'step': 4, 'filelist': ['campbell_backplane_c5a4_cpld_v01.svf'], 'pattern':r'campbell_backplane_c5a4_cpld_(v\d+).svf', 'chain_type': None,
                        'expected': {'filename':'campbell_backplane_c5a4_cpld_v01.svf', 'version':'0.1.0', 'build':False, 'verify':'pass'}},
                    {'step': 5, 'filelist': ['campbell_backplane_c5a4_cpld_v1.svf'], 'pattern':r'campbell_backplane_c5a4_cpld_(\d+v\d+).svf', 'chain_type': None,
                        'expected': {'filename':'campbell_backplane_c5a4_cpld_v1.svf', 'version':'0.1.0', 'build':False, 'verify':'pass'}},
                    {'step': 6, 'filelist': ['campbell_backplane_c5a4_cpld_v1.svf'], 'pattern':r'campbell_backplane_c5a4_cpld_(v\d+).svf', 'chain_type': None,
                        'expected': {'filename':'campbell_backplane_c5a4_cpld_v1.svf', 'version':'0.1.0', 'build':False, 'verify':'pass'}},
                    {'step': 7, 'filelist': ['campbell_backplane_c5a4_cpld_0v01.svf'], 'pattern':r'campbell_backplane_c5a4_cpld_(\d+v\d+).svf', 'chain_type': None,
                        'expected': {'filename':'campbell_backplane_c5a4_cpld_0v01.svf', 'version':'0.1.0', 'build':False, 'verify':'pass'}},
                    {'step': 8, 'filelist': ['campbell_backplane_c5a4_cpld_0v01.svf'], 'pattern':r'campbell_backplane_c5a4_cpld_(v\d+).svf', 'chain_type': None,
                        'expected': {'filename':'campbell_backplane_c5a4_cpld_0v01.svf', 'version':'0.1.0', 'build':False, 'verify':'fail_filename'}},
                    {'step': 9, 'filelist': ['campbell_motherboard_12v05.svf'], 'pattern':r'campbell_motherboard_(\d+v\d+).svf', 'chain_type': None,
                        'expected': {'filename':'campbell_motherboard_12v05.svf', 'version':'12.5.0', 'build':False, 'verify':'pass'}},
                    {'step':10, 'filelist': ['io_ethernet_2v08.6_kuka.rpd'], 'pattern':r'io_ethernet_(\d+v\d+)\.\d+_kuka(.ftdi|.v6jtag|).(rpd|svf)', 'chain_type': None,
                        'expected': {'filename':'io_ethernet_2v08.6_kuka.rpd', 'version':'2.8.0', 'build':False, 'verify':'pass'}},
                    {'step':11, 'filelist': ['io_ethernet_2v08.6_kuka.v6jtag.svf'], 'pattern':r'io_ethernet_(\d+v\d+)\.\d+_kuka(.ftdi|.v6jtag|).(rpd|svf)', 'chain_type': None,
                        'expected': {'filename':'io_ethernet_2v08.6_kuka.v6jtag.svf', 'version':'2.8.0', 'build':False, 'verify': 'pass'}},
                    {'step':12, 'filelist': ['pl650-update-tools-1.9.0R-74.deb'], 'pattern':r'pl650-update-tools-(\d+.\d+.\d+)(R|D)-(\d+).deb', 'chain_type': None,
                        'expected': {'filename':'pl650-update-tools-1.9.0R-74.deb', 'version':'1.9.0', 'build':False, 'verify':'pass'}},
                    {'step':13, 'filelist': ['pl650-update-tools-1.9.0R-74.deb'], 'pattern':r'pl650-update-tools-(\d+.\d+.\d+)(R|D)-(\d+).deb', 'chain_type': None,
                        'expected': {'filename':'pl650-update-tools-1.9.0R-74.deb', 'version':'1.9.0R-74', 'build':True, 'verify':'pass'}},
                    {'step':14, 'filelist': ['pl650-client-2.1.15R-320.deb'], 'pattern':r'pl650-client-(\d+.\d+.\d+)(R|D)-(\d+).deb', 'chain_type': None,
                        'expected': {'filename':'pl650-client-2.1.15R-320.deb', 'version':'2.1.15', 'build':False, 'verify':'pass'}},
                    {'step':15, 'filelist': ['pl650-client-2.1.15R-320.deb'], 'pattern':r'pl650-client-(\d+.\d+.\d+)(R|D)-(\d+).deb', 'chain_type': None,
                        'expected': {'filename':'pl650-client-2.1.15R-320.deb', 'version':'2.1.15R-320', 'build':True, 'verify':'pass'}},
                    {'step':16, 'filelist': ['pl650-firmware-1.9.0D-487.deb'], 'pattern':r'pl650-firmware-(\d+.\d+.\d+)(R|D)-(\d+).deb', 'chain_type': None,
                        'expected': {'filename':'pl650-firmware-1.9.0D-487.deb', 'version':'1.9.0', 'build':False, 'verify':'pass'}},
                    {'step':17, 'filelist': ['pl650-firmware-1.9.0D-487.deb'], 'pattern':r'pl650-firmware-(\d+.\d+.\d+)(R|D)-(\d+).deb', 'chain_type': None,
                        'expected': {'filename':'pl650-firmware-1.9.0D-487.deb', 'version':'1.9.0', 'build':False, 'verify':'pass'}},
                    {'step':18, 'filelist': ['pl650-firmware-1.9.0-487.deb'], 'pattern':r'pl650-firmware-(\d+.\d+.\d+)(R|D|)-(\d+).deb', 'chain_type': None,
                        'expected': {'filename':'pl650-firmware-1.9.0-487.deb', 'version':'1.9.0-487', 'build':True, 'verify':'pass'}},                             # added R|D|
                    {'step':19, 'filelist': ['pl650-firmware-1.9.0-487.deb'], 'pattern':r'pl650-firmware-(\d+.\d+.\d+)(R|D)-(\d+).deb', 'chain_type': None,
                        'expected': {'filename':'pl650-firmware-1.9.0-487.deb', 'version':'1.9.0-487', 'build':True, 'verify':'fail_filename'}},                   # R|D fail on filename
                    {'step':20, 'filelist': ['io_ethernet_2v08.6_kuka.rpd', 'io_ethernet_2v08.6_kuka.ftdi.svf', 'io_ethernet_2v08.6_kuka.v6jtag.svf'], 'pattern':r'io_ethernet_(\d+v\d+)\.\d+_kuka(.ftdi|.v6jtag|).(rpd|svf)','chain_type': None, 
                        'expected': {'filename':'io_ethernet_2v08.6_kuka.rpd', 'version':'2.8.0', 'build':False, 'verify':'pass'}},                                # find RPD
                    {'step':21, 'filelist': ['io_ethernet_2v08.6_kuka.rpd', 'io_ethernet_2v08.6_kuka.ftdi.svf', 'io_ethernet_2v08.6_kuka.v6jtag.svf'], 'pattern':r'io_ethernet_(\d+v\d+)\.\d+_kuka(.ftdi|.v6jtag|).(svf|rpd)', 'chain_type': 'ftdi', 
                        'expected': {'filename':'io_ethernet_2v08.6_kuka.ftdi.svf', 'version':'2.8.0', 'build':False, 'verify':'pass'}},                            # check prio: flip rpd/svf                   
                    {'step':22, 'filelist': ['a6_29v05.rpd', 'a6_29v05.ftdi.svf'], 'pattern':r'a6_(\d+v\d+)(.ftdi|.v6jtag|).(rpd|svf)', 'chain_type': None,
                        'expected': {'filename':'a6_29v05.rpd', 'version':'29.5.0', 'build':False, 'verify':'pass'}},                                               # find RPD
                    {'step':23, 'filelist': ['a6_29v05.rpd', 'a6_29v05.ftdi.svf'], 'pattern':r'a6_(\d+v\d+)(.ftdi|.v6jtag|).(svf|rpd)', 'chain_type': None,
                        'expected': {'filename':'a6_29v05.ftdi.svf', 'version':'29.5.0', 'build':False, 'verify':'pass'}},                                               # check prio: flip svf/rpd
                    {'step':24, 'filelist': ['a6_29v05.rpd', 'a6_32v04.ftdi.svf'], 'pattern':r'a6_(\d+v\d+)(.ftdi|.v6jtag|).(rpd|svf)', 'chain_type': None,
                        'expected': {'filename':'a6_32v04.ftdi.svf', 'version':'32.4.0', 'build':False, 'verify':'pass'}},                                                # take version for file extension prio
                    {'step':25, 'filelist': ['a6_32v04.ftdi.svf', 'a6_29v05.rpd'], 'pattern':r'a6_(\d+v\d+)(.ftdi|.v6jtag|).(rpd|svf)', 'chain_type': None,
                        'expected': {'filename':'a6_32v04.ftdi.svf', 'version':'32.4.0', 'build':False, 'verify':'pass'}},                                                # take version for file extension prio
                    {'step':26, 'filelist': ['a6_32v05.ftdi.svf', 'a6_32v04.ftdi.svf'], 'pattern':r'a6_(\d+v\d+)(.ftdi|.v6jtag|).(rpd|svf)', 'chain_type': None,
                        'expected': {'filename':'a6_32v05.ftdi.svf', 'version':'32.5.0', 'build':False, 'verify':'pass'}},     
                    {'step':27, 'filelist': ['pl650-firmware-1.9.0R-501.deb', 'pl650-firmware-1.9.0R-492.deb'], 'pattern':r'pl650-firmware-(\d+.\d+.\d+)(R|D)-(\d+).deb', 'chain_type': None,
                        'expected': {'filename':'pl650-firmware-1.9.0R-501.deb', 'version':'1.9.0R-501', 'build':True, 'verify':'pass'}},
    ]
    
    def create_file(self, filename):
        f = open(filename, "a")
        
        f.write("Now the file has more content!")
        f.close()    
    
    # def setUp(self):
    #     for test in self.test_list:
    #         self.create_file(test['filename'])

    def tearDown(self):
        for test in self.test_list:
            try:
                # delete
                for filename in test['filelist']:
                    delete_file(filename, interactive=False)
            except:
                pass

    def test_get_filename_and_version(self):
        for test in self.test_list:
            # create
            for filename in test['filelist']:
                self.create_file(filename)
            
            # get filename pattern
            pattern = test['pattern']         
            # handle special case
            if test['chain_type'] != None:
                if pattern.find('.ftdi|.v6jtag') != -1:
                    # in case of v6 jtag we search for filename pattern ".v6jtag"
                    if test['chain_type'] == 'v6jtag':
                        pattern = pattern.replace('.ftdi|', '')
                    # in case of ftdi we search for filename pattern ".ftdi"
                    elif test['chain_type'] == 'ftdi':
                        pattern = pattern.replace('|.v6jtag', '')
                elif pattern.find('.v6jtag|.ftdi') != -1:
                    # in case of v6 jtag we search for filename pattern ".v6jtag"
                    if test['chain_type'] == 'v6jtag':
                        pattern = pattern.replace('|.ftdi', '')
                    # in case of ftdi we search for filename pattern ".ftdi"
                    elif test['chain_type'] == 'ftdi':
                        pattern = pattern.replace('.v6jtag|', '')
                #print("Old pattern {}, New pattern {}".format(test['pattern'], pattern))
                
            # get filename
            ret_name = get_filename(path=os.getcwd(), pattern=pattern)
            #print(ret_name, test['filelist'])
            if test['expected']['verify']  == 'pass' or test['expected']['verify'] == 'fail_version':
                assert ret_name == test['expected']['filename'], "Wrong filename at step '{}'! Expected = '{}', Measured = '{}'".format(test['step'], test['expected']['filename'], ret_name)
            else:
                assert ret_name == None, "Wrong filename at step '{}'! Not expected = '{}', Measured = '{}'".format(test['step'], test['expected']['filename'], ret_name)
                    
            # get version
            if ret_name == None:
                ret_ver = get_version_from_filename(filename=test['expected']['filename'], with_build_info=test['expected']['build'])
            else:
                ret_ver = get_version_from_filename(ret_name, with_build_info=test['expected']['build'])
            #print(ret_ver, test['expected']['version'])
            if test['expected']['verify']  == 'pass' or test['expected']['verify']  == 'fail_filename':
                assert ret_ver == test['expected']['version'], "Wrong version at step '{}'! Expected = '{}', Measured = '{}'".format(test['step'], test['expected']['version'], ret_ver)
            else:
                assert ret_ver == None, "Wrong version at step '{}'! Not expected = '{}', Measured = '{}'".format(test['step'], test['expected']['version'], ret_ver)
            # delete
            for filename in test['filelist']:
                delete_file(filename, interactive=False)

if __name__ == "__main__":
    unittest.main()
    
