# examples from
# http://www.aerospaceweb.org/question/aerodynamics/q0252.shtml

import unittest
from vector2d import Vector2D
from sevenFourSeven import SevenFourSeven
from airfoil import Airfoil


class TestSevenFourSeven(unittest.TestCase):
    def test_airplane_lift(self):
        vel = Vector2D(265.5, 0)
        pos = Vector2D(200, 200)
        airplane = SevenFourSeven(pos, vel)
        airplane._theta = 0
        lift = airplane.airfoils()[0].calculateLift(airplane._theta, vel)

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
        airplane._theta = 0
        lift = airplane.airfoils()[0].calculateLift(airplane._theta, vel)

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
        airplane._theta = 0
        airplane.step(1)
        self.assertEqual(0, round(airplane._force.magnitude(), 2))

    def test_airplane_weight(self):
        airplane = SevenFourSeven(Vector2D(200, 200), Vector2D(265.3581764, 0))
        self.assertEqual(2833500, round(airplane.weight().magnitude(), 3))

    def test_airplane_Cl(self):
        vel = Vector2D(1, 1)
        airplane = SevenFourSeven(Vector2D(200, 200), vel)
        airplane._theta = 45
        airfoil = airplane.airfoils()[0]
        cl = airfoil.calculateCoefficientOfLift(airplane._theta, vel)

        self.assertEqual(.52, round(cl, 2))

    def test_airplane_AoA(self):

        airfoil = Airfoil("test", Vector2D(0, 0), 0, 0, 0, 0)

        self.assertEqual(-5, airfoil.calcAOA(5, 10), "1=>1-")
        self.assertEqual(-95, airfoil.calcAOA(5, 100), "1=>2-")
        self.assertEqual(-175, airfoil.calcAOA(10, 185), "1=>3-")
        self.assertEqual(175, airfoil.calcAOA(10, 195), "1=>3+")
        self.assertEqual(10, airfoil.calcAOA(5, 355), "1=>4+")

        self.assertEqual(90, airfoil.calcAOA(95, 5), "2=>1+")
        self.assertEqual(5, airfoil.calcAOA(100, 95), "2=>2+")
        self.assertEqual(-5, airfoil.calcAOA(95, 100), "2=>2-")
        self.assertEqual(-90, airfoil.calcAOA(95, 185), "2=>3-")
        self.assertEqual(105, airfoil.calcAOA(100, 355), "2=>4+")
        self.assertEqual(-175, airfoil.calcAOA(100, 275), "2=>4-")

        self.assertEqual(-175, airfoil.calcAOA(190, 5), "3=>1-")
        self.assertEqual(105, airfoil.calcAOA(190, 85), "3=>1-")
        self.assertEqual(20, airfoil.calcAOA(190, 170), "3=>2-")
        self.assertEqual(5, airfoil.calcAOA(190, 185), "3=>3-")
        self.assertEqual(-5, airfoil.calcAOA(190, 195), "3=>3+")
        self.assertEqual(-85, airfoil.calcAOA(190, 275), "3=>4+")

        self.assertEqual(-85, airfoil.calcAOA(280, 5), "4=>1-")
        self.assertEqual(-160, airfoil.calcAOA(280, 80), "4=>2-")
        self.assertEqual(-175, airfoil.calcAOA(280, 95), "4=>3-")
        self.assertEqual(175, airfoil.calcAOA(280, 105), "4=>3+")
        self.assertEqual(5, airfoil.calcAOA(280, 275), "4=>4+")
        self.assertEqual(-70, airfoil.calcAOA(280, 350), "4=>4-")

    # TODO - lift vector


# Some code to make the tests actually run.
if __name__ == '__main__':
    unittest.main()
