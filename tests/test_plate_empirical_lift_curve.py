import unittest
from flight.lift.plate_empirical import PlateEmpirical
from physics.angle import Angle


class TestPlateEmpiricalLiftCurve(unittest.TestCase):

    def test_neg_170(self):
        cl = PlateEmpirical(1).calculate_lift_coefficient(Angle(-170))
        self.assertAlmostEqual(-0.75854699, cl)

    def test_neg_100(self):
        cl = PlateEmpirical(1).calculate_lift_coefficient(Angle(-100))
        self.assertAlmostEqual(-0.17488299, cl)

    def test_neg_10(self):
        cl = PlateEmpirical(1).calculate_lift_coefficient(Angle(-10))
        self.assertAlmostEqual(-0.75854699, cl)

    def test_10(self):
        cl = PlateEmpirical(1).calculate_lift_coefficient(Angle(10))
        self.assertAlmostEqual(0.758546992, cl)

    def test_80(self):
        cl = PlateEmpirical(1).calculate_lift_coefficient(Angle(80))
        self.assertAlmostEqual(0.17488299, cl)

    def test_100(self):
        cl = PlateEmpirical(1).calculate_lift_coefficient(Angle(100))
        self.assertAlmostEqual(0.17488299, cl)

    def test_170(self):
        cl = PlateEmpirical(1).calculate_lift_coefficient(Angle(100))
        self.assertAlmostEqual(0.17488299, cl)


# Some code to make the tests actually run.
if __name__ == '__main__':
    unittest.main()
