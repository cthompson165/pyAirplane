# pylint: disable=missing-docstring
import unittest
from util.angle import Angle


class TestAngle(unittest.TestCase):

    def test_normalize(self):
        angle = Angle(100)
        self.assertEqual(100, angle.degrees())

    def test_normalize_over(self):
        angle = Angle(365)
        self.assertEqual(5, angle.degrees())

    def test_normalize_way_over(self):
        angle = Angle(725)
        self.assertEqual(5, angle.degrees())

    def test_normalize_under(self):
        angle = Angle(-5)
        self.assertEqual(355, angle.degrees())

    def test_normalize_way_under(self):
        angle = Angle(-365)
        self.assertEqual(355, angle.degrees())


if __name__ == '__main__':
    unittest.main()
