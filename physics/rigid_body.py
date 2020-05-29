from util.vector_2d import Vector2D
from physics.force import Force


class RigidBody:
    ''' Calculates state based on forces '''

    def __init__(self, mass, mass_moment_of_inertia, state):
        self._state = state
        self._mass = mass
        self._mass_moment_of_inertia = mass_moment_of_inertia
        self.body = None

    def mass(self):
        return self._mass

    def moment(self):
        return self._mass_moment_of_inertia

    def pos(self):
        return self._state.pos.copy()

    def orientation(self):
        return self._state.theta

    def current_state(self):
        return self._state.copy()

    def calculate_local_forces(self, local_velocity, angular_velocity):
        local_forces = []

        if self.surfaces() is not None:
            for surface in self.surfaces():
                local_forces.extend(
                    surface.calculate_forces(
                        local_velocity,
                        angular_velocity))

        return local_forces

    def calculate_global_forces(self, state):
        forces = []
        gravity = Force(Force.Source.gravity,
                        "gravity", state.pos, self.weight())
        forces.append(gravity)
        return forces

    def weight(self):
        return Vector2D(0, -9.8 * self.mass())
