from rigidBody import RigidBody
from vector import Vector2D
import math


class Airplane(RigidBody):

    air_density = 0.30267

    def wingArea(this):
        pass

    def wingSpan(this):
        pass

    # unused in favor of lift0 + stability derivative
    def coefficientOfLift(this):
        pass

    def coefficientOfLiftStabilityDerivative(this):
        pass

    def coefficientOfLift0(this):
        pass

    def mass(this):
        pass

    def massMomentOfInertia(this):
        pass

    def cg(this):
        return Vector2D([0, 0])

    def cp(this):
        pass

    def __init__(this, pos, vel):
        RigidBody.__init__(this, this.mass(), this.massMomentOfInertia(), pos,
                           0, vel, 0)

    def calcAOA(this, theta, vel_angle):

        # normalized is what theta is if vel_angle is 0
        normalized = theta - vel_angle

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

    def calculateLift(this):
        # equation from
        # http://www.aerospaceweb.org/question/aerodynamics/q0252.shtml
        vel_mag = this._vel.magnitude()
        return (Airplane.air_density * vel_mag**2 * this.wingArea() *
                this.calculateCoefficientOfLift()) / 2

    def calculateCoefficientOfLift(this):
        # C_l = C_la * a + C_l0
        aoa = this.calcAOA(this._theta, this._vel.angle())

        print ("aoa: " + str(aoa))
        print("aoa rads: " + str(math.radians(aoa)))

        C_l = this.coefficientOfLiftStabilityDerivative() * math.radians(aoa) + this.coefficientOfLift0()

        print ("CL: " + str(C_l))

        return C_l

    def lift(this):
        lift_mag = this.calculateLift()
        lift_dir = this._vel.rotate(90).unit()
        lift_force = lift_dir.scale(lift_mag)
        return lift_force

    def weight(this):
        return Vector2D([0, -9.8 * this.mass()])

    def step(this, t):
        this.resetForces()
  
        print("t: " + str(t))
        print("theta: " + str(round(this._theta, 3)))
        print("vel: " + str(this._vel.round(3)))
        print("lift: " + str(this.lift().round(3)))
        print("weight: " + str(this.weight().round(3)))
        print("angular vel: " + str(round(this._angularVel, 3)))

        this.addForce(this.cp(), this.lift())
        this.addForce(this.cg(), this.weight())

        this.move(t)


class SevenFourSeven(Airplane):
    def __init__(this, pos, vel):
        Airplane.__init__(this, pos, vel)

    def wingArea(this):
        return 510.97

    def cp(this):
        return Vector2D([-3, 0])

    def mass(this):
        return 289132.653061  # weight (F) / a (9.8)

    def massMomentOfInertia(this):
        length = 68.4
        height = 19.4
        return this.mass() * (length**2 + height**2) / 12  # rectangle...

    def wingSpan(this):
        return 59.74

    def coefficientOfLift(this):
        return 0.52

    def coefficientOfLiftStabilityDerivative(this):
        return 5.5

    def coefficientOfLift0(this):
        return 0.29
