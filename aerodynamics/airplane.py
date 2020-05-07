from util.vector2d import Vector2D
from util.angle import Angle
from physics.force import Force
from physics.state import State 
from physics.rigidBody import RigidBody

import math

class Airplane(RigidBody):

    def apply_pitch_control(self, percent):
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

    def calculate_thrust(self, state):
        pass

    def calculateForces(self, state):
       
        forces = []
        
        self.debugPrint(self.state)

        for surface in self.surfaces():
            
            self.debugPrint("-- " + surface.name + " --")
            
            velocity_rot = self.calculate_velocity_from_rotation(surface)
            surface_vel = state.vel.add(velocity_rot)

            self.debugPrint("vel: " + str(state.vel))
            self.debugPrint("theta vel: " + str(state.theta_vel))
            self.debugPrint("vel rot: " + str(velocity_rot))
            self.debugPrint("vel tot: " + str(surface_vel))
            self.debugPrint("vel tot angle: " + str(surface_vel.angle()))

            lift_mag = surface.calculate_lift(state.theta, surface_vel)
            lift_dir = surface_vel.rotate(Angle(90)).unit()
            lift_force = lift_dir.scale(lift_mag)

            drag_mag = surface.calculate_drag(state.theta, surface_vel)
            drag_dir = surface_vel.reverse().unit()
            drag_force = drag_dir.scale(drag_mag)

            self.debugPrint("AoA: " + str(surface.AoA(state.theta, surface_vel).relativeDegrees()))
            self.debugPrint("AoA ex: " + str(surface.AoA(state.theta, state.vel).relativeDegrees()))
            self.debugPrint("lift: " + str(lift_force))
            self.debugPrint("drag: " + str(drag_force))

            forces.append(Force("lift", surface.relative_pos, lift_force))
            forces.append(Force("drag", surface.relative_pos, drag_force))

        self.debugPrint ("----------------------------------------")

        thrust = self.calculate_thrust(self.state)
        print("thrust: " + str(thrust))
        forces.append(Force("thrust", self.cg(), thrust))
        forces.append(Force("gravity", self.cg(), self.weight()))

        print ("VEL: " + str(state.vel.magnitude()) + ": " + str(state.vel.angle().degrees()))

        return forces

    def calculate_velocity_from_rotation(self, surface):
        # TODO - this should go in surface which will need State
        # convert degrees per second (theta_vel) to meters per second

        # TODO - will we ever want CG not to be origin?
        if surface.relative_pos.x != 0 or surface.relative_pos.y != 0:

            magnitude = math.tan(math.radians(self.state.theta_vel)) * surface.distance_to_cg

            # get a vector 90 degrees from relative pos that points in the
            # direction of positive rotation.

             # TODO: can cache this
            tangent_vel_unit = surface.relative_pos.rotate(Angle(90)).unit()
            return tangent_vel_unit.scale(magnitude)
        else:
            return Vector2D(0, 0)

    def weight(self):
        return Vector2D(0, -9.8 * self.mass())

    def debugPrint(self, message):
        if self.debug:
            print (message)

