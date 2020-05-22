# boeing examples from
# http://www.aerospaceweb.org/question/aerodynamics/q0252.shtml

# cessna from
# http://www.aerospaceweb.org/question/aerodynamics/q0184.shtml

import unittest
from aerodynamics.lift_curves.linear_lift import LinearLift
from aerodynamics.lift_curves.lifting_line_lift import LiftingLineLift
from aerodynamics.drag_curves.lifting_line_drag import LiftingLineDrag

from util.angle import Angle


class TestForceCurves(unittest.TestCase):

    def get_747_lift_curve(self):
        return LinearLift(6.98, 0.29, 5.5)

    def get_747_drag_curve(self):
        return LiftingLineDrag(6.98, 0.0305, 0.75)

    def get_cessna_lift_curve(self):
        return LiftingLineLift(7.37)

    def get_cessna_drag_curve(self):
        return LiftingLineDrag(7.37, 0.027, 0.75)

    def test_cl_boeing(self):
        lift_curve = self.get_747_lift_curve()
        coefficient_lift = lift_curve.calculate_lift_coefficient(Angle(2.4))
        self.assertEqual(.52, round(coefficient_lift, 2))

    def test_cla_lifting_line(self):
        lift_curve = LiftingLineLift(7.37)
        self.assertAlmostEqual(4.942, lift_curve.lift_slope_3d, 3)

    def test_cl_cesna(self):
        lift_curve = self.get_cessna_lift_curve()

        coefficient_lift = lift_curve.calculate_lift_coefficient(Angle(0))
        self.assertAlmostEqual(0, coefficient_lift, 4, "0")

        coefficient_lift = lift_curve.calculate_lift_coefficient(Angle(1))
        self.assertAlmostEqual(0.086255169, coefficient_lift, 4, "1")

        coefficient_lift = lift_curve.calculate_lift_coefficient(Angle(6))
        self.assertAlmostEqual(0.517531017, coefficient_lift, 4, "6")

        coefficient_lift = lift_curve.calculate_lift_coefficient(Angle(12))
        self.assertAlmostEqual(1.035062034, coefficient_lift, 4, "12")

        coefficient_lift = lift_curve.calculate_lift_coefficient(Angle(15))
        self.assertAlmostEqual(1.293827542, coefficient_lift, 4, "15")

    def test_cd_cesna(self):
        drag_curve = self.get_cessna_drag_curve()
        lift_curve = self.get_cessna_lift_curve()

        coefficient_lift = lift_curve.calculate_lift_coefficient(Angle(0))
        coefficient_drag = drag_curve.calculate_drag_coefficient(
            Angle(0),
            coefficient_lift)
        self.assertAlmostEqual(0.027, coefficient_drag, 4, "0")

        coefficient_lift = lift_curve.calculate_lift_coefficient(Angle(1))
        coefficient_drag = drag_curve.calculate_drag_coefficient(
            Angle(1),
            coefficient_lift)
        self.assertAlmostEqual(0.02742, coefficient_drag, 4, "1")

        coefficient_lift = lift_curve.calculate_lift_coefficient(Angle(6))
        coefficient_drag = drag_curve.calculate_drag_coefficient(
            Angle(6),
            coefficient_lift)
        self.assertAlmostEqual(0.04242, coefficient_drag, 4, "6")


# Some code to make the tests actually run.
if __name__ == '__main__':
    unittest.main()
