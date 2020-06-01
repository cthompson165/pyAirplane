import unittest
import math
from util.vector_2d import Vector2D
from util.angle import Angle


class TestVector(unittest.TestCase):
    def test_add(self):
        vec = Vector2D(2, 2)
        vec_2 = Vector2D(0, 3)
        self.assertTrue(Vector2D(2, 5).equals(vec.add(vec_2)))

    def test_subtract(self):
        vec = Vector2D(5, 4)
        vec_2 = Vector2D(1, 3)
        self.assertTrue(Vector2D(4, 1).equals(vec.subtract(vec_2)))

    def test_scale(self):
        vec = Vector2D(3, 5)
        vec_2 = vec.scale(4)
        self.assertEqual(12, vec_2.x)
        self.assertEqual(20, vec_2.y)

    def test_scale_div(self):
        vec = Vector2D(30, 50)
        vec_2 = vec.scale(1.0/10)
        self.assertEqual(3, vec_2.x)
        self.assertEqual(5, vec_2.y)

    def test_angle_with_other(self):
        vec = Vector2D(2, 2)
        vec_2 = Vector2D(0, 3)
        self.assertAlmostEqual(45, vec.angle_with_other(vec_2).degrees())

    def test_angle(self):
        # 45s
        vec = Vector2D(1, 1)
        self.assertAlmostEqual(45, vec.angle().degrees())

        vec = Vector2D(-1, 1)
        self.assertAlmostEqual(135, vec.angle().degrees())

        vec = Vector2D(-1, -1)
        self.assertAlmostEqual(225, vec.angle().degrees())

        vec = Vector2D(1, -1)
        self.assertAlmostEqual(315, vec.angle().degrees())

        # 90s
        vec = Vector2D(1, 0)
        self.assertAlmostEqual(0, vec.angle().degrees())

        vec = Vector2D(0, 1)
        self.assertAlmostEqual(90, vec.angle().degrees())

        vec = Vector2D(-1, 0)
        self.assertAlmostEqual(180, vec.angle().degrees())

        vec = Vector2D(0, -1)
        self.assertAlmostEqual(270, vec.angle().degrees())

    def test_rotate_90(self):
        vec = Vector2D(1, 0)
        u_rot = vec.rotate(Angle(90)).round(2)
        expected = Vector2D(0, 1)
        self.assertTrue(expected.equals(u_rot))

    def test_rotate_45(self):
        vec = Vector2D(1, 0)
        u_rot = vec.rotate(Angle(45))
        self.assertAlmostEqual(0.70710678, u_rot.x)
        self.assertAlmostEqual(0.70710678, u_rot.y)

    def test_unit(self):
        vec = Vector2D(-2, 1)
        expected = Vector2D(-2 / math.sqrt(5), 1 / math.sqrt(5)).round(2)
        self.assertTrue(expected.equals(vec.unit().round(2)))

    def test_unit_0(self):
        vec = Vector2D(0, 0).unit()
        self.assertEqual(0, vec.x)
        self.assertEqual(0, vec.y)

    def test_dot(self):
        vec = Vector2D(5, 12)
        vec_2 = Vector2D(-6, 8)
        self.assertEqual(66, vec.dot(vec_2))

    def test_mag(self):
        vec = Vector2D(2, 3)
        self.assertAlmostEqual(math.sqrt(13), vec.magnitude())

    def test_mag_0(self):
        vec = Vector2D(0, 0)
        mag = vec.magnitude()
        self.assertAlmostEqual(0, mag)

    def test_cross(self):
        vec = Vector2D(5, 13)
        vec_2 = Vector2D(7, 17)
        self.assertEqual(-6, vec.cross(vec_2))

    def test_reverse(self):
        rev = Vector2D(5, 13).reverse()
        self.assertEqual(-5, rev.x)
        self.assertEqual(-13, rev.y)


# Some code to make the tests actually run.
if __name__ == '__main__':
    unittest.main()
