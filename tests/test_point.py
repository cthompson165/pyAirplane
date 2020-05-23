import unittest
from util.vector_2d import Vector2D
from physics.point import Point


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


# Some code to make the tests actually run.
if __name__ == '__main__':
    unittest.main()
