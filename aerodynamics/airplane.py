from util.vector_2d import Vector2D
from util.angle import Angle
from physics.force import Force
from physics.state import State
from physics.rigid_body import RigidBody


class Airplane(RigidBody):

    def apply_pitch_control(self, percent):
        pass

    def mass(self):
        pass

    def mass_moment_of_inertia(self):
        pass

    def surfaces(self):
        pass

    def cg(self):
        return Vector2D(0, 0)

    def __init__(self, pos, vel):
        state = State(pos, vel, Angle(0), 0)
        RigidBody.__init__(self, self.mass(),
                           self.mass_moment_of_inertia(), state)
        self.debug = False

    def pos(self):
        return self.state.pos

    def orientation(self):
        return self.state.theta

    def calculate_thrust(self, state):
        pass

    def calculate_forces(self, state):

        forces = []

        for surface in self.surfaces():
            forces.extend(surface.calculate_forces(self.state))

        forces.append(
            Force("thrust", self.cg(), self.calculate_thrust(self.state)))
        forces.append(Force("gravity", self.cg(), self.weight()))

        return forces

    def weight(self):
        return Vector2D(0, -9.8 * self.mass())

    def debug_print(self, message):
        if self.debug:
            print(message)
