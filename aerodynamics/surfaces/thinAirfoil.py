from aerodynamics.surface import Surface

class ThinAirfoil(Surface):

    def __init__(self, name, relative_pos, relative_degrees, area, CLa, CL0):
        Surface.__init__(self, name, relative_pos, relative_degrees, area)
        self.CLa = CLa
        self.CL0 = CL0

    def calculateCoefficientOfLift(self, airplaneAngle, velocity):
        aoa = self.AoA(airplaneAngle, velocity)

        # thin airfoil
        # CL = CLa * AoA + CL0
        CL = self.CLa * aoa.relativeRadians() + self.CL0
        return CL

