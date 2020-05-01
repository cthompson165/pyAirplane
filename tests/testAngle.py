import unittest
from util.angle import Angle


class TestAngle(unittest.TestCase):

    def testNormalize(self):
        angle = Angle(100)
        self.assertEqual(100, angle.degrees())

    def testNormalizeOver(self):
        angle = Angle(365)
        self.assertEqual(5, angle.degrees())

    def testNormalizeWayOver(self):
        angle = Angle(725)
        self.assertEqual(5, angle.degrees())
    
    def testNormalizeUnder(self):
        angle = Angle(-5)
        self.assertEqual(355, angle.degrees())
    
    def testNormalizeWayUnder(self):
        angle = Angle(-365)
        self.assertEqual(355, angle.degrees())
   

if __name__ == '__main__':
    unittest.main()