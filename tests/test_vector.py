import unittest
import math
from vector2d import Vector2D


class TestVector(unittest.TestCase):
    def test_vector_add(self):
        u = Vector2D(2, 2)
        v = Vector2D(0, 3)
        self.assertTrue(Vector2D(2, 5).equals(u.add(v)))

    def test_vector_subtract(self):
        u = Vector2D(5, 4)
        v = Vector2D(1, 3)
        self.assertTrue(Vector2D(4, 1).equals(u.subtract(v)))

    def test_vector_scale(self):
        u = Vector2D(3, 5)
        v = u.scale(4)
        self.assertEqual(12, v.x)
        self.assertEqual(20, v.y)

    def test_vector_scale_div(self):
        u = Vector2D(30, 50)
        v = u.scale(1.0/10)
        self.assertEqual(3, v.x)
        self.assertEqual(5, v.y)

    def test_vector_angleWithOther(self):
        u = Vector2D(2, 2)
        v = Vector2D(0, 3)
        self.assertAlmostEqual(45, u.angle_with_other(v))

    def test_vector_angle(self):
        # 45s
        u = Vector2D(1, 1)
        self.assertAlmostEqual(45, u.angle())

        u = Vector2D(-1, 1)
        self.assertAlmostEqual(135, u.angle())

        u = Vector2D(-1, -1)
        self.assertAlmostEqual(225, u.angle())

        u = Vector2D(1, -1)
        self.assertAlmostEqual(315, u.angle())

        # 90s
        u = Vector2D(1, 0)
        self.assertAlmostEqual(0, u.angle())

        u = Vector2D(0, 1)
        self.assertAlmostEqual(90, u.angle())

        u = Vector2D(-1, 0)
        self.assertAlmostEqual(180, u.angle())

        u = Vector2D(0, -1)
        self.assertAlmostEqual(270, u.angle())

    def test_vector_rotate(self):
        u = Vector2D(1, 0)
        u_rot = u.rotate(90).round(2)
        expected = Vector2D(0, 1)
        self.assertTrue(expected.equals(u_rot))

    def test_vector_unit(self):
        u = Vector2D(-2, 1)
        expected = Vector2D(-2 / math.sqrt(5), 1 / math.sqrt(5)).round(2)
        self.assertTrue(expected.equals(u.unit().round(2)))

    def test_vector_dot(self):
        u = Vector2D(5, 12)
        v = Vector2D(-6, 8)
        self.assertEqual(66, u.dot(v))

    def test_vector_mag(self):
        u = Vector2D(2, 3)
        self.assertAlmostEqual(math.sqrt(13), u.magnitude())

    def test_vector_cross(self):
        u = Vector2D(5, 13)
        v = Vector2D(7, 17)
        self.assertEqual(-6, u.cross(v))


# Some code to make the tests actually run.
if __name__ == '__main__':
    unittest.main()
