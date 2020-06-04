from util.vector_2d import Vector2D
from physics.force import Force


class RigidBody:
    ''' Calculates state based on forces '''

    def __init__(self, mass, mass_moment_of_inertia, state):
        self._state = state
        self._mass = mass
        self._mass_moment_of_inertia = mass_moment_of_inertia
        self.body = None
        self.key = 0

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

    def local_to_global(self, position):
        return position.rotate(self.orientation()).add(self.pos())

    def calculate_surface_forces(self, local_velocity, angular_velocity):
        surface_forces = []

        if self.surfaces() is not None:
            for surface in self.surfaces():
                surface_forces.extend(
                    surface.calculate_forces(
                        local_velocity,
                        angular_velocity))

        return surface_forces

    def calculate_thrust_forces(self):
        return None

    def calculate_weight_force(self, state):
        weight = Force(Force.Source.gravity,
                       "weight", state.pos, self.weight())
        return weight

    def weight(self):
        return Vector2D(0, -9.8 * self.mass())
