'''
Created on Oct 17, 2014

@author: khuyen
'''
import unittest
import parser

class Test(unittest.TestCase):
    
    def setUp(self):
        """This method will be run before each of the test methods in the class."""
        self.parser = parser.LineParser()
        
    def tearDown(self):
        pass
    
    def testParser(self):
        file_name = 'mips_hex.txt'
        test_data = open(file_name, 'r').readlines()
        for line in test_data:
            self.parser.Parse(line)
            print self.parser.mem_address, self.parser.bin_instr


    if __name__ == "__main__":
        #import sys;sys.argv = ['', 'Test.testTranslate']
        unittest.main()