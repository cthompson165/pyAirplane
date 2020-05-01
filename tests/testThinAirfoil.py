# examples from
# http://www.aerospaceweb.org/question/aerodynamics/q0252.shtml

import unittest
from util.vector2d import Vector2D
from aerodynamics.surfaces.thinAirfoil import ThinAirfoil
from util.angle import Angle


class TestAirfoil(unittest.TestCase):
    def getWing(self):
        return ThinAirfoil("wing", Vector2D(0, 0), 2.4, 510.97, 5.5, 0.29)

    def testLift(self):

        vel = Vector2D(265.5, 0)
        lift = self.getWing().calculateLift(Angle(0), vel)

        # example's rounding was pretty far off
        # when using Cl calculated from stability
        # derivative. Verified the following expected result
        # in excel. Difference is with Cl being 0.520383461
        # vs. 0.52

        self.assertEqual(2836530, round(lift, 0))

    def testCl(self):
        vel = Vector2D(1, 1)
        airfoil = self.getWing()
        cl = airfoil.calculateCoefficientOfLift(Angle(45), vel)

        self.assertEqual(.52, round(cl, 2))

    # TODO - lift vector


# Some code to make the tests actually run.
if __name__ == '__main__':
    unittest.main()
