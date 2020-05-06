# boeing examples from
# http://www.aerospaceweb.org/question/aerodynamics/q0252.shtml

# cessna from
# http://www.aerospaceweb.org/question/aerodynamics/q0184.shtml

import unittest
from util.vector2d import Vector2D
from aerodynamics.surfaces.thinAirfoil import ThinAirfoil
from util.angle import Angle


class TestAirfoil(unittest.TestCase):
    def get_boeing_wing(self):
        return ThinAirfoil("boeing wing", Vector2D(0, 0), 2.4, 510.97, 6.98, 5.5, 0.29, 0.0305, 0.75)

    def get_cessna_wing(self):
        return ThinAirfoil("cessna 172 wing", Vector2D(0, 0), 0, 16.2, 7.37, 0, 0, 0.027, 0.75)

    def test_Cl_boeing(self):
        vel = Vector2D(1, 1)
        airfoil = self.get_boeing_wing()
        cl = airfoil.calculate_lift_coefficient(Angle(45), vel)

        self.assertEqual(.52, round(cl, 2))

    def test_CLa_lifting_line(self):
        wing = self.get_cessna_wing()
        CLa = wing.calculate_CLa_lifting_line(7.37)
        self.assertAlmostEqual(4.942, CLa, 3)
    
    def test_CL_cesna(self):
        wing = self.get_cessna_wing()

        CL = wing.calculate_lift_coefficient(Angle(0), Vector2D(100, 0))
        self.assertAlmostEqual(0, CL, 4, "0")
        
        CL = wing.calculate_lift_coefficient(Angle(1), Vector2D(100, 0))
        self.assertAlmostEqual(0.086255169, CL, 4, "1")

        CL = wing.calculate_lift_coefficient(Angle(6), Vector2D(100, 0))
        self.assertAlmostEqual(0.517531017, CL, 4, "6")

        CL = wing.calculate_lift_coefficient(Angle(12), Vector2D(100, 0))
        self.assertAlmostEqual(1.035062034, CL, 4, "12")

        CL = wing.calculate_lift_coefficient(Angle(15), Vector2D(100, 0))
        self.assertAlmostEqual(1.293827542, CL, 4, "15")

    def test_CD_cesna(self):
        wing = self.get_cessna_wing()

        CD = wing.calculate_drag_coefficient(Angle(0), Vector2D(100, 0))
        self.assertAlmostEqual(0.027, CD, 4, "0")

        CD = wing.calculate_drag_coefficient(Angle(1), Vector2D(100, 0))
        self.assertAlmostEqual(0.027428442, CD, 4, "1")

        CD = wing.calculate_drag_coefficient(Angle(6), Vector2D(100, 0))
        self.assertAlmostEqual(0.042423898, CD, 4, "6")

# Some code to make the tests actually run.
if __name__ == '__main__':
    unittest.main()
