from util.vector_2d import Vector2D
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

    def calculate_local_forces(self, local_velocity, angular_velocity):
        local_forces = super().calculate_local_forces(
            local_velocity, angular_velocity)

        if self.engines() is not None:
            for engine in self.engines():
                local_forces.append(engine.get_thrust())
        return local_forces

    def engines(self):
        raise NotImplementedError

    def surfaces(self):
        raise NotImplementedError

    def cg(self):
        return Vector2D(0, 0)
