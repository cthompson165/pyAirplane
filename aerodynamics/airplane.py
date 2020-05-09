from util.vector_2d import Vector2D
from physics.force import Force
from physics.rigid_body import RigidBody


class Airplane(RigidBody):

    def __init__(self, initial_state, mass, mass_moment_of_inertia):
        RigidBody.__init__(self, mass,
                           mass_moment_of_inertia, initial_state)
        self.debug = False

    def apply_pitch_control(self, percent):
        raise NotImplementedError

    def set_throttle(self, percent):
        raise NotImplementedError

    def calculate_thrust(self, state):
        raise NotImplementedError

    def surfaces(self):
        raise NotImplementedError

    def cg(self):
        return Vector2D(0, 0)

    def current_state(self):
        return self.state.copy()

    def pos(self):
        return self.state.pos

    def orientation(self):
        return self.state.theta

    def calculate_forces(self, state):

        forces = []

        for surface in self.surfaces():
            forces.extend(surface.calculate_forces(self.state))

        forces.append(
            Force(Force.Source.thrust, "thrust", self.cg(),
                  self.calculate_thrust(self.state)))
        forces.append(Force(Force.Source.gravity,
                            "gravity", self.cg(), self.weight()))

        return forces

    def weight(self):
        return Vector2D(0, -9.8 * self.mass())
