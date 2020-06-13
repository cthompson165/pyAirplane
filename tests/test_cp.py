import unittest
from physics.vector_2d import Vector2D
from physics.angle import Angle
from aerodynamics.cp import CP


class TestCP(unittest.TestCase):

    def test_0_length(self):
        cp = CP(Vector2D(1, 0), 0, Angle(10))
        calculated = cp.calculate(Angle(1))
        self.assertEqual(1, calculated.x)

    def test_null_angle(self):
        cp = CP(Vector2D(1, 0), 12, None)
        calculated = cp.calculate(Angle(1))
        self.assertEqual(1, calculated.x)

    def test_normal(self):
        cp = CP(Vector2D(1, 0), 12, Angle(10))
        calculated = cp.calculate(Angle(1))
        self.assertEqual(-2, calculated.x)

    def test_stalled(self):
        cp = CP(Vector2D(1, 0), 12, Angle(10))
        calculated = cp.calculate(Angle(50))
        self.assertEqual(-3.5, calculated.x)

    def test_vertical(self):
        cp = CP(Vector2D(1, 0), 12, Angle(10))
        calculated = cp.calculate(Angle(90))
        self.assertEqual(-5, calculated.x)

    def test_just_past_vertical(self):
        cp = CP(Vector2D(1, 0), 12, Angle(10))
        calculated = cp.calculate(Angle(91))
        self.assertEqual(-5.0375, calculated.x)

    def test_backward_stalled(self):
        cp = CP(Vector2D(1, 0), 12, Angle(10))
        calculated = cp.calculate(Angle(130))
        self.assertEqual(-6.5, calculated.x)

    def test_backward(self):
        cp = CP(Vector2D(1, 0), 12, Angle(10))
        calculated = cp.calculate(Angle(175))
        self.assertEqual(-8, calculated.x)

    def test_down(self):
        cp = CP(Vector2D(1, 0), 12, Angle(10))
        calculated = cp.calculate(Angle(-5))
        self.assertEqual(-2, calculated.x)

    def test_down_stalled(self):
        cp = CP(Vector2D(1, 0), 12, Angle(10))
        calculated = cp.calculate(Angle(-50))
        self.assertEqual(-3.5, calculated.x)

    def test_down_vertical(self):
        cp = CP(Vector2D(1, 0), 12, Angle(10))
        calculated = cp.calculate(Angle(-90))
        self.assertEqual(-5, calculated.x)

    def test_backward_upsidedown_stalled(self):
        cp = CP(Vector2D(1, 0), 12, Angle(10))
        calculated = cp.calculate(Angle(-130))
        self.assertEqual(-6.5, calculated.x)

    def test_backward_upsidedown(self):
        cp = CP(Vector2D(1, 0), 12, Angle(10))
        calculated = cp.calculate(Angle(-175))
        self.assertEqual(-8, calculated.x)


# Some code to make the tests actually run.
if __name__ == '__main__':
    unittest.main()
