import unittest
from physics.vector_2d import Vector2D
from physics.point import Point
import math


class TestPoint(unittest.TestCase):

    def test_velocity_rear(self):

        point = Point(Vector2D(-10, 0))
        velocity = point.total_velocity(Vector2D(0, 0), 3)

        self.assertAlmostEqual(-0.524, velocity.y, 3)
        self.assertAlmostEqual(0, velocity.x)

    def test_velocity_forward(self):

        point = Point(Vector2D(10, 0))
        velocity = point.total_velocity(Vector2D(0, 0), 3)

        self.assertAlmostEqual(0.524, velocity.y, 3)
        self.assertAlmostEqual(0, velocity.x)

    def test_velocity_1_rotation(self):
        point = Point(Vector2D(10, 0))

        # rotate 360 degree / second
        velocity = point.total_velocity(Vector2D(0, 0), 360)

        # speed = circumference
        speed = 2 * math.pi * 10

        self.assertAlmostEqual(speed, velocity.y, 3)
        self.assertAlmostEqual(0, velocity.x)

    def test_velocity_2_rotations(self):
        point = Point(Vector2D(10, 0))

        # rotate 360 degree / second
        velocity = point.total_velocity(Vector2D(0, 0), 720)

        # speed = circumference
        speed = 4 * math.pi * 10

        self.assertAlmostEqual(speed, velocity.y, 3)
        self.assertAlmostEqual(0, velocity.x)



# Some code to make the tests actually run.
if __name__ == '__main__':
    unittest.main()
