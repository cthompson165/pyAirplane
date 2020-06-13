import math
from flight.lift.linear import Linear
from physics.angle import Angle


class LiftingLine(Linear):
    ''' Use if you know the 2d lift coefficients or take
    the defaults. Uses lifting line theory to estimate 3d coefficient'''

    TWO_PI = math.pi * 2

    def __init__(self, aspect_ratio, CL0=0, lift_slope_2d=TWO_PI):

        Linear.__init__(
            self, aspect_ratio, CL0,
            LiftingLine.calculate_3d_lift_slope(
                aspect_ratio, lift_slope_2d))

    def calculate_3d_lift_slope(aspect_ratio, lift_slope2d):
        return lift_slope2d * (aspect_ratio / (2 + aspect_ratio))

    def stall_angle(self):
        return Angle(20)  # TODO
