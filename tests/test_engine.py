import unittest
from physics.vector_2d import Vector2D
from physics.angle import Angle
from flight.engine import Engine


class TestEngine(unittest.TestCase):

    def test_simple(self):
        engine = Engine("test", Vector2D(0, 0), Angle(0), 0, 100)
        engine.set_throttle(80)
        self.assertEqual(80, engine.get_thrust().vector.x)

    def test_with_idle(self):
        engine = Engine("test", Vector2D(0, 0), Angle(0), 20, 100)
        engine.set_throttle(50)
        self.assertEqual(60, engine.get_thrust().vector.x)

    def test_with_angle(self):
        engine = Engine("test", Vector2D(0, 0), Angle(45), 0, 100)
        engine.set_throttle(80)
        thrust = engine.get_thrust().vector
        self.assertAlmostEqual(56.57, thrust.x, 2)
        self.assertAlmostEqual(56.57, thrust.y, 2)


# Some code to make the tests actually run.
if __name__ == '__main__':
    unittest.main()
