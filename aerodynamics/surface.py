class Surface:

    air_density = 0.30267

    def __init__(self, name, relativePos, relativeDegrees, area):

        self.name = name
        self.relativePos = relativePos  # relative to CG
        self.relativeDegrees = relativeDegrees
        self.area = area

    def calcAOA(self, angle, velAngle):
        return angle.minus(velAngle)

    def AoA(self, airplaneAngle, velocity):
        absoluteAngle = airplaneAngle.plusConstant(self.relativeDegrees)

        velAngle = velocity.angle()
        return self.calcAOA(absoluteAngle, velAngle)

    def calculateLift(self, airplaneAngle, velocity):

        # equation from
        # http://www.aerospaceweb.org/question/aerodynamics/q0252.shtml
        CL =  self.calculateCoefficientOfLift(airplaneAngle, velocity)

        vel_mag = velocity.magnitude()
        lift = (Surface.air_density * vel_mag**2 * self.area * CL) / 2

        return lift

    def calculateCoefficientOfLift(self, airplaneAngle, velocity):
        pass

