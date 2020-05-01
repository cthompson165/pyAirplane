from util.vector2d import Vector2D
from util.angle import Angle
from physics.force import Force
from physics.state import State 
from physics.rigidBody import RigidBody

class Airplane(RigidBody):

    def setElevatorTo(self, degrees):
        pass

    def mass(self):
        pass

    def massMomentOfInertia(self):
        pass

    def surfaces(self):
        pass

    def cg(self):
        return Vector2D(0, 0)

    def __init__(self, pos, vel):
        state = State(pos, vel, Angle(0), 0)
        RigidBody.__init__(self, self.mass(), self.massMomentOfInertia(), state)
        self.debug = False

    def pos(self):
        return self.state.pos

    def orientation(self):
        return self.state.theta

    def calculateForces(self, state):
       
        forces = []
        
        self.debugPrint(self.state)

        for surface in self.surfaces():
            
            self.debugPrint("-- " + surface.name + " --")
            
            lift_mag = surface.calculateLift(state.theta, state.vel)
            lift_dir = state.vel.rotate(Angle(90)).unit()
            lift_force = lift_dir.scale(lift_mag)

            self.debugPrint("AoA: " + str(surface.AoA(state.theta, state.vel).relativeDegrees()))
            self.debugPrint("lift: " + str(lift_force))
            
            forces.append(Force(surface.relative_pos, lift_force))

        self.debugPrint ("----------------------------------------")

        # gravity
        forces.append(Force(self.cg(), self.weight()))

        return forces

    def weight(self):
        return Vector2D(0, -9.8 * self.mass())

    def debugPrint(self, message):
        if self.debug:
            print (message)

