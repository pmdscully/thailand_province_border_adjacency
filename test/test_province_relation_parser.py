default_path = "../src/"
import sys
sys.path.insert(0, default_path)
import unittest

from province_neighbours import read_provincial_dataset, read_relations_dataset, Province, ProvinceRelationParser

class Test_ProvinceRelationParser(unittest.TestCase):
    
    def __init__(self, *args, **kwords):
        unittest.TestCase.__init__(self, *args, **kwords)
        self.provincial_lookup = read_provincial_dataset( filename="../phannisa_province_data_latlon_v02_utf8.csv" )

    

    def test_invalid_province_name_list(self):
        """"""
        s = "Nong Khai -> Bueng Kan, Udon Thani, Sakon Nakhon, Loei"
        s1 = "Bueng Kan -> Nakhon Phanom, Sakon Nakhon, Nong Khai, sss"
        data = [s,"",s1]
        prp = ProvinceRelationParser(data, self.provincial_lookup)
        actual = prp._province_naming_errors
        actual2 = prp._relation_error
        expected = ['Missing Province Lookup: Province> BUENG KAN: (26, 38, BUENG KAN, บึงกาฬ) -> SSS']
        expected2 = ['1. Missing Province Neighbour Entry for NONG KHAI -> UDON THANI.', '1. Missing Province Neighbour Entry for NONG KHAI -> SAKON NAKHON.', '1. Missing Province Neighbour Entry for NONG KHAI -> LOEI.', '2. Missing Province Neighbour Entry for BUENG KAN -> NAKHON PHANOM.', '2. Missing Province Neighbour Entry for BUENG KAN -> SAKON NAKHON.', '2. Missing Province Neighbour Entry for BUENG KAN -> **INVALID**.']
        self.assertTrue(actual == expected)
        self.assertTrue(actual2 == expected2)

    def test_list_mutual_positions(self):
        data = ["Nong Khai -> Bueng Kan", 
                "Bueng Kan -> Nong Khai" ]
        prp = ProvinceRelationParser(data, self.provincial_lookup)
        actual = prp._province_naming_errors
        actual2 = prp._relation_error
        expected = []
        expected2 = []
        self.assertTrue(actual == expected)
        self.assertTrue(actual2 == expected2)
        
    def test_list_invalid_mutual_positions(self):
        data = ["Nong Khai -> Bueng Kan", 
                "Bueng Kan -> Nong Khai, Nakhon Phanom",
                "Nakhon Phanom -> Bueng Kan, Nong Khai" ] # Mutual relation missing for Bueng Kan.
        prp = ProvinceRelationParser(data, self.provincial_lookup)
        actual = prp._province_naming_errors
        actual2 = prp._relation_error
        expected = []
        expected2 = ['3. Missing Mutual Neighbour for NAKHON PHANOM -> NONG KHAI.']
        self.assertTrue(actual == expected)
        self.assertTrue(actual2 == expected2)
        


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromModule( sys.modules[__name__] )
    unittest.TextTestRunner(verbosity=3).run(suite)
        
