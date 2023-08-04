import unittest

import sys
from pathlib import Path

# >> add folders to syspath
sys.path.insert(0, str(Path(Path(__file__).parent, "..")))
# << add folders to syspath

# own imports
from type_handling import check_for_duplicates, convert_to_int_list

class TestTypeHandling(unittest.TestCase):
    # def setUp(self):
    #     self.v6jtag = V6JTAGER()

    # def tearDown(self):
    #     self.v6jtag.close()

    def test_duplicate(self):
        assert(check_for_duplicates([0,1]) == False)
        assert(check_for_duplicates([1,1]) == True)

    def test_convert_to_int_list(self):
        assert(convert_to_int_list([0,1,2,3,4,5,6,7]) == [0,1,2,3,4,5,6,7])
        assert(convert_to_int_list([1]) == [1])
        assert(convert_to_int_list(1) == [1])
        assert(convert_to_int_list([0, 1]) == [0,1])
        assert(convert_to_int_list('1') == [1])
        assert(convert_to_int_list('2') == [2])
        assert(convert_to_int_list('0,1') == [0,1])
        assert(convert_to_int_list('0, 1') == [0,1])
        assert(convert_to_int_list('[0, 1]') == [0,1])
        assert(convert_to_int_list('[0,1]') == [0,1])
        self.assertRaises(ValueError, convert_to_int_list, '1,1')

if __name__ == "__main__":
    unittest.main()