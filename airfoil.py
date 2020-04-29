import math

class Airfoil:

    air_density = 0.30267

    def __init__(self, name, relativePos, relativeAoA, area, CLa, CL0):

        self.name = name
        self.relativePos = relativePos  # relative to CG
        self.relativeAoA = relativeAoA
        self.area = area
        self.CLa = CLa
        self.CL0 = CL0

        self.debugPrint = False

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
        lift = (Airfoil.air_density * vel_mag**2 * self.area * CL) / 2

        if self.debugPrint:
            print ("lift: " + str(lift))
            print ("-----")

        return lift

    def calculateCoefficientOfLift(self, airplaneAngle, velocity):

        absoluteAoA = self.calculateAbsoluteAoA(airplaneAngle)

        vel_angle = velocity.angle()
        aoa = self.calcAOA(absoluteAoA, vel_angle)

        # thin airfoil
        # CL = CLa * AoA + CL0
        CL = self.CLa * math.radians(aoa) + self.CL0

        if self.debugPrint:
          print ("relative AOA: " + str(self.relativeAoA))
          print ("absolute AOA: " + str(absoluteAoA))
          print ("AOA: " + str(aoa))
          print ("CL: " + str(CL))
          
        
        return CL

    def calculateAbsoluteAoA(self, airplaneAngle):
        # TODO - test this

        absoluteAoA = airplaneAngle + self.relativeAoA
        while absoluteAoA >= 360:
            absoluteAoA -= 360
        while absoluteAoA < 0:
            absoluteAoA += 360
        return absoluteAoA

