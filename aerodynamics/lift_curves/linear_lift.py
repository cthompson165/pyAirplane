from aerodynamics.lift_curve import LiftCurve


class LinearLift(LiftCurve):
    ''' Use if you know the 3d lift coefficient.'''

    def __init__(self, aspect_ratio, CL0, lift_slope_3d):
        self.aspect_ratio = aspect_ratio
        self.CL0 = CL0
        self.lift_slope_3d = lift_slope_3d

    def calculate_lift_coefficient(self, aoa):
        return self.CL0 + self.lift_slope_3d * aoa.relative_radians()
