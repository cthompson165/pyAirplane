import unittest
from util.vector_2d import Vector2D
from physics.state import State
from physics.point import Point


class TestPoint(unittest.TestCase):

    def test_velocity_rear(self):

        point = Point(Vector2D(-10, 0))
        vel = point.total_velocity(Vector2D(0, 0), 3)

        self.assertAlmostEqual(-0.524, vel.y, 3)
        self.assertAlmostEqual(0, vel.x)

    def test_velocity_forward(self):

        point = Point(Vector2D(10, 0))
        vel = point.total_velocity(Vector2D(0, 0), 3)

        self.assertAlmostEqual(0.524, vel.y, 3)
        self.assertAlmostEqual(0, vel.x)


# Some code to make the tests actually run.
if __name__ == '__main__':
    unittest.main()
