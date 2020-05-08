# boeing examples from
# http://www.aerospaceweb.org/question/aerodynamics/q0252.shtml

# cessna from
# http://www.aerospaceweb.org/question/aerodynamics/q0184.shtml

import unittest
from util.vector_2d import Vector2D
from aerodynamics.lift_curves.linear_lift import LinearLift
from aerodynamics.lift_curves.lifting_line_lift import LiftingLineLift
from aerodynamics.drag_curves.lifting_line_drag import LiftingLineDrag

from util.angle import Angle


class TestAirfoil(unittest.TestCase):

    def get_747_lift_curve(self):
        return LinearLift(6.98, 0.29, 5.5)

    def get_747_drag_curve(self):
        return LiftingLineDrag(6.98, 0.0305, 0.75)

    def get_cessna_lift_curve(self):
        return LiftingLineLift(7.37)

    def get_cessna_drag_curve(self):
        return LiftingLineDrag(7.37, 0.027, 0.75)
        
    def test_Cl_boeing(self):
        lift_curve = self.get_747_lift_curve()
        cl = lift_curve.calculate_lift_coefficient(Angle(2.4))
        self.assertEqual(.52, round(cl, 2))

    def test_CLa_lifting_line(self):
        lift_curve = LiftingLineLift(7.37)
        self.assertAlmostEqual(4.942, lift_curve.lift_slope_3d, 3)
    
    def test_CL_cesna(self):
        lift_curve = self.get_cessna_lift_curve()

        CL = lift_curve.calculate_lift_coefficient(Angle(0))
        self.assertAlmostEqual(0, CL, 4, "0")
        
        CL = lift_curve.calculate_lift_coefficient(Angle(1))
        self.assertAlmostEqual(0.086255169, CL, 4, "1")

        CL = lift_curve.calculate_lift_coefficient(Angle(6))
        self.assertAlmostEqual(0.517531017, CL, 4, "6")

        CL = lift_curve.calculate_lift_coefficient(Angle(12))
        self.assertAlmostEqual(1.035062034, CL, 4, "12")

        CL = lift_curve.calculate_lift_coefficient(Angle(15))
        self.assertAlmostEqual(1.293827542, CL, 4, "15")

    def test_CD_cesna(self):
        drag_curve = self.get_cessna_drag_curve()
        lift_curve = self.get_cessna_lift_curve()

        CL = lift_curve.calculate_lift_coefficient(Angle(0))
        CD = drag_curve.calculate_drag_coefficient(CL)
        self.assertAlmostEqual(0.027, CD, 4, "0")

        CL = lift_curve.calculate_lift_coefficient(Angle(1))
        CD = drag_curve.calculate_drag_coefficient(CL)
        self.assertAlmostEqual(0.02742, CD, 4, "1")

        CL = lift_curve.calculate_lift_coefficient(Angle(6))
        CD = drag_curve.calculate_drag_coefficient(CL)
        self.assertAlmostEqual(0.04242, CD, 4, "6")

# Some code to make the tests actually run.
if __name__ == '__main__':
    unittest.main()
