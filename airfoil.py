import math

class Airfoil:

    air_density = 0.30267

    def __init__(self, relativePos, relativeAoA, area, CLa, CL0):

        self.relativePos = relativePos
        self.relativeAoA = relativeAoA
        self.area = area
        self.CLa = CLa
        self.CL0 = CL0

    def calcAOA(self, angle, vel_angle):

        # normalized is what theta is if vel_angle is 0
        normalized = angle - vel_angle

        if normalized > 0:
            # AOA is positive until plane flips completely
            # over going backward
            if normalized <= 180:
                return normalized
            else:
                return normalized - 360
        else:
            if normalized >= -180:
                return normalized
            else:
                return 360 + normalized

    def calculateLift(self, airplaneAngle, velocity):

        # equation from
        # http://www.aerospaceweb.org/question/aerodynamics/q0252.shtml
        CL =  self.calculateCoefficientOfLift(airplaneAngle, velocity)

        vel_mag = velocity.magnitude()
        return (Airfoil.air_density * vel_mag**2 * self.area * CL) / 2

    def calculateCoefficientOfLift(self, airplaneAngle, velocity):

        totalAngle = airplaneAngle + self.relativeAoA
        vel_angle = velocity.angle()
        aoa = self.calcAOA(totalAngle, vel_angle)

        # thin airfoil
        # CL = CLa * AoA + CL0
        CL = self.CLa * math.radians(aoa) + self.CL0
        return CL
