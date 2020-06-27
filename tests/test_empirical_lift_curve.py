import unittest
from flight.lift.empirical import Empirical
from physics.vector_2d import Vector2D
from physics.angle import Angle


class FakeLiftCurve(Empirical):
    def __init__(self):
        Empirical.__init__(self)

    def get_points(self):
        points = []
        points.append(Vector2D(-180, 0))
        points.append(Vector2D(-170, -2))
        points.append(Vector2D(-160, -3))
        points.append(Vector2D(-90, 0))
        points.append(Vector2D(-20, -3))
        points.append(Vector2D(-10, -2))
        points.append(Vector2D(0, 0))
        points.append(Vector2D(10, 2))
        points.append(Vector2D(20, 3))
        points.append(Vector2D(90, 0))
        points.append(Vector2D(160, 3))
        points.append(Vector2D(170, 2))
        points.append(Vector2D(180, 0))
        return points


class TestEmpiricalLiftCurve(unittest.TestCase):

    def test_0(self):
        cl = FakeLiftCurve().calculate_lift_coefficient(Angle(0))
        self.assertEqual(0, cl)

    def test_5(self):
        cl = FakeLiftCurve().calculate_lift_coefficient(Angle(5))
        self.assertEqual(1, cl)

    def test_9(self):
        cl = FakeLiftCurve().calculate_lift_coefficient(Angle(9))
        self.assertEqual(1.8, cl)

    def test_11(self):
        cl = FakeLiftCurve().calculate_lift_coefficient(Angle(11))
        self.assertEqual(2.1, cl)

    def test_85(self):
        cl = FakeLiftCurve().calculate_lift_coefficient(Angle(85))
        self.assertAlmostEqual(0.214, cl, 3)

    def test_90(self):
        cl = FakeLiftCurve().calculate_lift_coefficient(Angle(90))
        self.assertEqual(0, cl)

    def test_95(self):
        cl = FakeLiftCurve().calculate_lift_coefficient(Angle(95))
        self.assertAlmostEqual(0.214, cl, 3)

    def test_180(self):
        cl = FakeLiftCurve().calculate_lift_coefficient(Angle(180))
        self.assertEqual(0, cl)

    def test_185(self):
        cl = FakeLiftCurve().calculate_lift_coefficient(Angle(185))
        self.assertEqual(-1, cl)

    def test_360(self):
        cl = FakeLiftCurve().calculate_lift_coefficient(Angle(360))
        self.assertEqual(0, cl)

    def test_355(self):
        cl = FakeLiftCurve().calculate_lift_coefficient(Angle(355))
        self.assertEqual(-1, cl)


# Some code to make the tests actually run.
if __name__ == '__main__':
    unittest.main()
