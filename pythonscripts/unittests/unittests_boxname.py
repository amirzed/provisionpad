import sys
sys.path.append('../')
import unittest
from boxno import r, get_box_name

class TestStringMethods(unittest.TestCase):

    def testjustinsetion(self):
        avn   = 'avn_test'
        instc = 'inst_c_test'
        r.delete(avn)
        r.set(instc, '0')
        self.assertEqual(get_box_name(avn, instc), 'box1')
        self.assertEqual(get_box_name(avn, instc), 'box2')
        self.assertEqual(get_box_name(avn, instc), 'box3')

    def testinsetiondeleted(self):
        avn   = 'avn_test'
        instc = 'inst_c_test'
        r.delete(avn)
        r.rpush(avn, 'box2')
        r.set(instc, '3')
        self.assertEqual(get_box_name(avn, instc), 'box2')
        self.assertEqual(get_box_name(avn, instc), 'box4')
        self.assertEqual(get_box_name(avn, instc), 'box5')

if __name__ == '__main__':
    unittest.main()