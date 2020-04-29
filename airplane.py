from rigidBody import RigidBody
from vector2d import Vector2D
from airfoil import Airfoil
import math
from force import Force

class Airplane(RigidBody):

    def changeElevator(self, angle):
        pass

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

    def calculateForces(self, pos, vel, theta, thetaVel):
       
        forces = []
        #print("vel: " + str(vel))
        #print("vel mag: " + str(vel.magnitude()))
        #print("theta: " + str(round(theta, 3)))
        #print("weight: " + str(self.weight().round(3)))

        for airfoil in self.airfoils():
            
            #print ("-- " + airfoil.name + " --")
            
            lift_mag = airfoil.calculateLift(theta, vel)
            lift_dir = vel.rotate(90).unit()
            lift_force = lift_dir.scale(lift_mag)

            if (airfoil.debugPrint):
                print ("lift: " + str(lift_force))
            
            forces.append(Force(airfoil.relativePos, lift_force))

        #print ("----------------------------------------")

        # gravity
        forces.append(Force(self.cg(), self.weight()))

        return forces

    def weight(self):
        return Vector2D(0, -9.8 * self.mass())

