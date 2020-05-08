# pylint: disable=missing-docstring
import unittest
import math
from util.vector_2d import Vector2D
from util.angle import Angle


class TestVector(unittest.TestCase):
    def test_add(self):
        vec_1 = Vector2D(2, 2)
        vec_2 = Vector2D(0, 3)
        self.assertTrue(Vector2D(2, 5).equals(vec_1.add(vec_2)))

    def test_subtract(self):
        vec_1 = Vector2D(5, 4)
        vec_2 = Vector2D(1, 3)
        self.assertTrue(Vector2D(4, 1).equals(vec_1.subtract(vec_2)))

    def test_scale(self):
        vec_1 = Vector2D(3, 5)
        vec_2 = vec_1.scale(4)
        self.assertEqual(12, vec_2.x)
        self.assertEqual(20, vec_2.y)

    def test_scale_div(self):
        vec_1 = Vector2D(30, 50)
        vec_2 = vec_1.scale(1.0/10)
        self.assertEqual(3, vec_2.x)
        self.assertEqual(5, vec_2.y)

    def test_angle_with_other(self):
        vec_1 = Vector2D(2, 2)
        vec_2 = Vector2D(0, 3)
        self.assertAlmostEqual(45, vec_1.angle_with_other(vec_2).degrees())

    def test_angle(self):
        # 45s
        vec_1 = Vector2D(1, 1)
        self.assertAlmostEqual(45, vec_1.angle().degrees())

        vec_1 = Vector2D(-1, 1)
        self.assertAlmostEqual(135, vec_1.angle().degrees())

        vec_1 = Vector2D(-1, -1)
        self.assertAlmostEqual(225, vec_1.angle().degrees())

        vec_1 = Vector2D(1, -1)
        self.assertAlmostEqual(315, vec_1.angle().degrees())

        # 90s
        vec_1 = Vector2D(1, 0)
        self.assertAlmostEqual(0, vec_1.angle().degrees())

        vec_1 = Vector2D(0, 1)
        self.assertAlmostEqual(90, vec_1.angle().degrees())

        vec_1 = Vector2D(-1, 0)
        self.assertAlmostEqual(180, vec_1.angle().degrees())

        vec_1 = Vector2D(0, -1)
        self.assertAlmostEqual(270, vec_1.angle().degrees())

    def test_rotate(self):
        vec_1 = Vector2D(1, 0)
        u_rot = vec_1.rotate(Angle(90)).round(2)
        expected = Vector2D(0, 1)
        self.assertTrue(expected.equals(u_rot))

    def test_unit(self):
        vec_1 = Vector2D(-2, 1)
        expected = Vector2D(-2 / math.sqrt(5), 1 / math.sqrt(5)).round(2)
        self.assertTrue(expected.equals(vec_1.unit().round(2)))

    def test_dot(self):
        vec_1 = Vector2D(5, 12)
        vec_2 = Vector2D(-6, 8)
        self.assertEqual(66, vec_1.dot(vec_2))

    def test_mag(self):
        vec_1 = Vector2D(2, 3)
        self.assertAlmostEqual(math.sqrt(13), vec_1.magnitude())

    def test_cross(self):
        vec_1 = Vector2D(5, 13)
        vec_2 = Vector2D(7, 17)
        self.assertEqual(-6, vec_1.cross(vec_2))

    def test_reverse(self):
        rev = Vector2D(5, 13).reverse()
        self.assertEqual(-5, rev.x)
        self.assertEqual(-13, rev.y)


# Some code to make the tests actually run.
if __name__ == '__main__':
    unittest.main()
