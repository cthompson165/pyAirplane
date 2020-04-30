from rigidBody import RigidBody
from vector2d import Vector2D
from airfoil import Airfoil
import math
from force import Force
from state import State 

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
        state = State(pos, vel, 0, 0)
        RigidBody.__init__(self, self.mass(), self.massMomentOfInertia(), state)
        self.debug = False

    def pos(self):
        return self.state.pos

    def orientation(self):
        return self.state.theta

    def calculateForces(self, state):
       
        forces = []
        
        self.debugPrint(self.state)

        for airfoil in self.airfoils():
            
            self.debugPrint("-- " + airfoil.name + " --")
            
            lift_mag = airfoil.calculateLift(state.theta, state.vel)
            lift_dir = state.vel.rotate(90).unit()
            lift_force = lift_dir.scale(lift_mag)

            self.debugPrint("AoA: " + str(airfoil.calculateAbsoluteAoA(state.theta)))
            self.debugPrint("lift: " + str(lift_force))
            
            forces.append(Force(airfoil.relativePos, lift_force))

        self.debugPrint ("----------------------------------------")

        # gravity
        forces.append(Force(self.cg(), self.weight()))

        return forces

    def weight(self):
        return Vector2D(0, -9.8 * self.mass())

    def debugPrint(self, message):
        if self.debug:
            print (message)

