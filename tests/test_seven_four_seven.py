# pylint: disable=missing-docstring
import unittest
from util.vector_2d import Vector2D
from aerodynamics.airplanes.seven_four_seven import SevenFourSeven

class TestSevenFourSeven(unittest.TestCase):

    def test_forces_balance(self):
        vel = Vector2D(265.3581764, 0)
        pos = Vector2D(200, 200)
        airplane = SevenFourSeven(pos, vel)
        airplane.step(1)
        self.assertEqual(0, round(airplane.state.vel.y, 2))

    def test_weight(self):
        airplane = SevenFourSeven(Vector2D(200, 200), Vector2D(265.3581764, 0))
        self.assertEqual(2833500, round(airplane.weight().magnitude(), 3))

# Some code to make the tests actually run.
if __name__ == '__main__':
    unittest.main()
