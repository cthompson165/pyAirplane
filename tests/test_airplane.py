# examples from
# http://www.aerospaceweb.org/question/aerodynamics/q0252.shtml

import unittest
from util.vector2d import Vector2D
from aerodynamics.airplanes.sevenFourSeven import SevenFourSeven
from aerodynamics.surfaces.thinAirfoil import ThinAirfoil
from util.angle import Angle
import math

class TestSevenFourSeven(unittest.TestCase):
    def test_airplane_lift(self):
        vel = Vector2D(265.5, 0)
        pos = Vector2D(200, 200)
        airplane = SevenFourSeven(pos, vel)

        lift = airplane.surfaces()[0].calculateLift(Angle(0), vel)

        # example's rounding was pretty far off
        # when using Cl calculated from stability
        # derivative. Verified the following expected result
        # in excel. Difference is with Cl being 0.520383461
        # vs. 0.52

        self.assertEqual(2836530, round(lift, 0))

    def test_airplane_balanced(self):
        vel = Vector2D(265.3581764, 0)
        pos = Vector2D(200, 200)
        airplane = SevenFourSeven(pos, vel)
        lift = airplane.surfaces()[0].calculateLift(Angle(0), vel)

        # example's rounding was pretty far off
        # when using Cl calculated from stability
        # derivative. Verified the following expected result
        # in excel. Difference is with Cl being 0.520383461
        # vs. 0.52

        self.assertEqual(
            round(airplane.weight().magnitude(), 2), round(lift, 2))

    def test_airplane_forces_balanced(self):
        vel = Vector2D(265.3581764, 0)
        pos = Vector2D(200, 200)
        airplane = SevenFourSeven(pos, vel)
        airplane.step(1)
        self.assertEqual(0, round(airplane.state.vel.y, 2))

    def test_airplane_weight(self):
        airplane = SevenFourSeven(Vector2D(200, 200), Vector2D(265.3581764, 0))
        self.assertEqual(2833500, round(airplane.weight().magnitude(), 3))

    def test_airplane_Cl(self):
        vel = Vector2D(1, 1)
        airplane = SevenFourSeven(Vector2D(200, 200), vel)
        airfoil = airplane.surfaces()[0]
        cl = airfoil.calculateCoefficientOfLift(Angle(45), vel)

        self.assertEqual(.52, round(cl, 2))

    def calcAOA(airfoil, a1, a2):
        return math.degrees(airfoil.calcAOA(Angle(a1), Angle(a2)).relativeRadians())

    def test_airplane_AoA(self):

        airfoil = ThinAirfoil("test", Vector2D(0, 0), 0, 0, 0, 0)

        self.assertAlmostEqual(-5, TestSevenFourSeven.calcAOA(airfoil, 5, 10), msg="1=>1-")
        self.assertAlmostEqual(-95, TestSevenFourSeven.calcAOA(airfoil, 5, 100), msg="1=>2-")
        self.assertAlmostEqual(-175, TestSevenFourSeven.calcAOA(airfoil, 10, 185), msg="1=>3-")
        self.assertAlmostEqual(175, TestSevenFourSeven.calcAOA(airfoil, 10, 195), msg="1=>3+")
        self.assertAlmostEqual(10, TestSevenFourSeven.calcAOA(airfoil, 5, 355), msg="1=>4+")

        self.assertAlmostEqual(90, TestSevenFourSeven.calcAOA(airfoil, 95, 5), msg="2=>1+")
        self.assertAlmostEqual(5, TestSevenFourSeven.calcAOA(airfoil, 100, 95), msg="2=>2+")
        self.assertAlmostEqual(-5, TestSevenFourSeven.calcAOA(airfoil, 95, 100), msg="2=>2-")
        self.assertAlmostEqual(-90, TestSevenFourSeven.calcAOA(airfoil, 95, 185), msg="2=>3-")
        self.assertAlmostEqual(105, TestSevenFourSeven.calcAOA(airfoil, 100, 355), msg="2=>4+")
        self.assertAlmostEqual(-175, TestSevenFourSeven.calcAOA(airfoil, 100, 275), msg="2=>4-")

        self.assertAlmostEqual(-175, TestSevenFourSeven.calcAOA(airfoil, 190, 5), msg="3=>1-")
        self.assertAlmostEqual(105, TestSevenFourSeven.calcAOA(airfoil, 190, 85), msg="3=>1-")
        self.assertAlmostEqual(20, TestSevenFourSeven.calcAOA(airfoil, 190, 170), msg="3=>2-")
        self.assertAlmostEqual(5, TestSevenFourSeven.calcAOA(airfoil, 190, 185), msg="3=>3-")
        self.assertAlmostEqual(-5, TestSevenFourSeven.calcAOA(airfoil, 190, 195), msg="3=>3+")
        self.assertAlmostEqual(-85, TestSevenFourSeven.calcAOA(airfoil, 190, 275), msg="3=>4+")

        self.assertAlmostEqual(-85, TestSevenFourSeven.calcAOA(airfoil, 280, 5), msg="4=>1-")
        self.assertAlmostEqual(-160, TestSevenFourSeven.calcAOA(airfoil, 280, 80), msg="4=>2-")
        self.assertAlmostEqual(-175, TestSevenFourSeven.calcAOA(airfoil, 280, 95), msg="4=>3-")
        self.assertAlmostEqual(175, TestSevenFourSeven.calcAOA(airfoil, 280, 105), msg="4=>3+")
        self.assertAlmostEqual(5, TestSevenFourSeven.calcAOA(airfoil, 280, 275), msg="4=>4+")
        self.assertAlmostEqual(-70, TestSevenFourSeven.calcAOA(airfoil, 280, 350), msg="4=>4-")
        

    # TODO - lift vector


# Some code to make the tests actually run.
if __name__ == '__main__':
    unittest.main()
