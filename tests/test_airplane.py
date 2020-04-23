# examples from
# http://www.aerospaceweb.org/question/aerodynamics/q0252.shtml

import unittest
from vector import Vector2D
from airplane import SevenFourSeven


class TestSevenFourSeven(unittest.TestCase):
    def test_airplane_lift(self):
        airplane = SevenFourSeven(Vector2D([200, 200]),
                                  Vector2D([265.5, 0]))
        airplane._theta = 2.4
        lift = airplane.calculateLift()

        # example's rounding was pretty far off
        # when using Cl calculated from stability
        # derivative. Verified the following expected result
        # in excel. Difference is with Cl being 0.520383461
        # vs. 0.52

        self.assertEqual(2836530, round(lift, 0))

    def test_airplane_balanced(self):
        airplane = SevenFourSeven(Vector2D([200, 200]),
                                  Vector2D([265.3581764, 0]))
        airplane._theta = 2.4
        lift = airplane.calculateLift()

        # example's rounding was pretty far off
        # when using Cl calculated from stability
        # derivative. Verified the following expected result
        # in excel. Difference is with Cl being 0.520383461
        # vs. 0.52

        self.assertEqual(round(airplane.weight().magnitude(), 2), round(lift, 2))

    def test_airplane_forces_balanced(self):
        airplane = SevenFourSeven(Vector2D([200, 200]),
                                  Vector2D([265.3581764, 0]))
        airplane._theta = 2.4
        airplane.step(1)
        self.assertEqual(0, round(airplane._force.magnitude(), 2))

    def test_airplane_weight(self):
        airplane = SevenFourSeven(Vector2D([200, 200]),
                                  Vector2D([265.3581764, 0]))
        self.assertEqual(2833500, round(airplane.weight().magnitude(), 3)
        )

    def test_airplane_Cl(self):
        airplane = SevenFourSeven(Vector2D([200, 200]),
                                  Vector2D([1, 1]))
        airplane._theta = 47.4  # 2.4 degrees above vel vector
        cl = airplane.calculateCoefficientOfLift()

        self.assertEqual(.52, round(cl, 2))

    def test_airplane_AoA(self):
        # cases
        #   1: |diff| < 180
        #   2:     

        #'''
        airplane = SevenFourSeven(Vector2D([200, 200]),
                                  Vector2D([1, 1]))
        self.assertEqual(-5, airplane.calcAOA(5, 10), "1=>1-")
        self.assertEqual(-95, airplane.calcAOA(5, 100), "1=>2-")
        self.assertEqual(-175, airplane.calcAOA(10, 185), "1=>3-")   
        self.assertEqual(175, airplane.calcAOA(10, 195), "1=>3+")
        self.assertEqual(10, airplane.calcAOA(5, 355), "1=>4+")

        self.assertEqual(90, airplane.calcAOA(95, 5), "2=>1+")
        self.assertEqual(5, airplane.calcAOA(100, 95), "2=>2+")
        self.assertEqual(-5, airplane.calcAOA(95, 100), "2=>2-")
        self.assertEqual(-90, airplane.calcAOA(95, 185), "2=>3-")
        self.assertEqual(105, airplane.calcAOA(100, 355), "2=>4+")
        self.assertEqual(-175, airplane.calcAOA(100, 275), "2=>4-")

        self.assertEqual(-175, airplane.calcAOA(190, 5), "3=>1-")
        self.assertEqual(105, airplane.calcAOA(190, 85), "3=>1-")
        self.assertEqual(20, airplane.calcAOA(190, 170), "3=>2-")
        self.assertEqual(5, airplane.calcAOA(190, 185), "3=>3-")
        self.assertEqual(-5, airplane.calcAOA(190, 195), "3=>3+")
        self.assertEqual(-85, airplane.calcAOA(190, 275), "3=>4+")

        self.assertEqual(-85, airplane.calcAOA(280, 5), "4=>1-")
        self.assertEqual(-160, airplane.calcAOA(280, 80), "4=>2-")
        self.assertEqual(-175, airplane.calcAOA(280, 95), "4=>3-")
        self.assertEqual(175, airplane.calcAOA(280, 105), "4=>3+")
        self.assertEqual(5, airplane.calcAOA(280, 275), "4=>4+")
        self.assertEqual(-70, airplane.calcAOA(280, 350), "4=>4-")

    # TODO - lift vector

# Some code to make the tests actually run.
if __name__ == '__main__':
    unittest.main()