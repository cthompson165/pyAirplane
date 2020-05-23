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

    def convert_local_forces_to_global(state, local_forces):
        global_forces = []
        for local_force in local_forces:
            global_forces.append(local_force.rotate(state.theta))
        return global_forces

    def caculate_local_forces(self, local_velocity, angular_velocity):
        local_forces = []

        if self.surfaces() is not None:
            for surface in self.surfaces():
                local_forces.extend(
                    surface.calculate_forces(
                        local_velocity,
                        angular_velocity))

        if self.engines() is not None:
            for engine in self.engines():
                local_forces.append(engine.get_thrust())
        return local_forces

    def calculate_global_forces(self, state):
        forces = []
        gravity = Force(Force.Source.gravity,
                        "gravity", self.cg(), self.weight())
        forces.append(gravity)
        return forces

    def calculate_forces(self, state, atmosphere):
        local_velocity = RigidBody.get_local_airspeed(state)
        local_forces = self.caculate_local_forces(
            local_velocity, state.theta_vel)
        forces = Airplane.convert_local_forces_to_global(state, local_forces)
        forces.extend(self.calculate_global_forces(state))
        return forces

    def weight(self):
        return Vector2D(0, -9.8 * self.mass())
