from rigidBody import RigidBody
from vector2d import Vector2D
from airfoil import Airfoil
import math


class Airplane(RigidBody):

    def mass(self):
        pass

    def massMomentOfInertia(self):
        pass

    def airfoils(self):
        pass

    def cg(self):
        return Vector2D(0, 0)

    def __init__(self, pos, vel):
        RigidBody.__init__(self, self.mass(), self.massMomentOfInertia(), pos,
                           0, vel, 0)

    

    def addLiftForces(self):

        for airfoil in self.airfoils():
            lift_mag = airfoil.calculateLift(self._theta, self._vel)
            lift_dir = self._vel.rotate(90).unit()
            lift_force = lift_dir.scale(lift_mag)
            
            self.addForce(airfoil.relativePos, lift_force)

    def weight(self):
        return Vector2D(0, -9.8 * self.mass())

    def step(self, t):
        self.resetForces()

        #print("t: " + str(t))
        #print("theta: " + str(round(self._theta, 3)))
        #print("vel: " + str(self._vel.round(3)))
        #print("lift: " + str(self.lift().round(3)))
        #print("weight: " + str(self.weight().round(3)))
        #print("angular vel: " + str(round(self._angularVel, 3)))

        self.addLiftForces()
        self.addForce(self.cg(), self.weight())

        self.move(t)

