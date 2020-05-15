from util.vector_2d import Vector2D
from physics.force import Force
from physics.rigid_body import RigidBody


class Airplane(RigidBody):

    def __init__(self, initial_state, mass, mass_moment_of_inertia):
        RigidBody.__init__(
            self, mass,
            mass_moment_of_inertia,
            initial_state)

    def apply_pitch_control(self, percent):
        raise NotImplementedError

    def set_throttle(self, percent):
        if self.engines() is not None:
            for engine in self.engines():
                engine.set_throttle(percent)

    def engines(self):
        raise NotImplementedError

    def surfaces(self):
        raise NotImplementedError

    def cg(self):
        return Vector2D(0, 0)

    def pos(self):
        return self.state.pos.copy()

    def orientation(self):
        return self.state.theta

    def calculate_local_forces(self, local_velocity, angular_velocity):

        forces = []

        if self.surfaces() is not None:
            for surface in self.surfaces():
                forces.extend(
                    surface.calculate_forces(
                        local_velocity,
                        angular_velocity))

        if self.engines() is not None:
            for engine in self.engines():
                forces.append(engine.get_thrust())

        return forces

    def calculate_global_forces(self, state):
        ''' Get forces that don't really make sense in a local reference frame.
            Like gravity... '''

        forces = []
        gravity = Force(Force.Source.gravity,
                        "gravity", self.cg(), self.weight())
        forces.append(gravity)
        return forces

    def weight(self):
        return Vector2D(0, -9.8 * self.mass())
