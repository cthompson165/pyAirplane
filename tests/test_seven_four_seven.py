import unittest
from util.vector_2d import Vector2D
from aerodynamics.simulator import Simulator
from aerodynamics.airplanes.seven_four_seven import SevenFourSeven


class TestSevenFourSeven(unittest.TestCase):

    def test_forces_balance(self):
        velocity = Vector2D(265.3581764, 0)
        position = Vector2D(200, 200)
        airplane = SevenFourSeven(position, velocity)
        simulator = Simulator()
        simulator.register_flying_object(airplane)

        simulator.step(1)
        self.assertEqual(0, round(airplane.airspeed().y, 2))

    def test_weight(self):
        airplane = SevenFourSeven(Vector2D(200, 200), Vector2D(265.3581764, 0))
        self.assertEqual(2833500, round(airplane.weight().magnitude(), 3))


# Some code to make the tests actually run.
if __name__ == '__main__':
    unittest.main()
