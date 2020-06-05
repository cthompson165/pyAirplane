from util.vector_2d import Vector2D
from physics.force import Force


class FlyingObject:
    ''' Calculates state based on forces '''

    def __init__(self, mass, mass_moment_of_inertia, state):
        self._state = state
        self._mass = mass
        self._mass_moment_of_inertia = mass_moment_of_inertia
        self._weight = Vector2D(0, -9.8 * self._mass)
        self.body = None
        self.key = 0

        self.step_forces = []
        self.step_local_forces = []

    def mass(self):
        return self._mass

    def moment(self):
        return self._mass_moment_of_inertia

    def position(self):
        return self._state.position

    def velocity(self):
        return self._state.velocity

    def airspeed(self):
        return self._state.airspeed()

    def orientation(self):
        return self._state.orientation

    def angular_velocity(self):
        return self._state.angular_velocity

    def global_forces(self):
        return self.step_forces

    def local_forces(self):
        return self.step_local_forces

    def clear_forces(self):
        self.step_forces.clear()
        self.step_local_forces.clear()

    def add_local_forces(self, forces):
        for force in forces:
            self.add_local_force(force.name, force.position, force.vector)

    def add_local_force(self, name, position, vector):
        self.step_local_forces.append(Force(name, position, vector))

    def add_global_force(self, name, position, vector):
        self.step_forces.append(Force(name, position, vector))

    def local_to_global(self, position):
        return position.rotate(self.orientation()).add(self.position())

    def calculate_surface_forces(self, local_velocity, angular_velocity):
        surface_forces = []

        if self.surfaces() is not None:
            for surface in self.surfaces():
                self.add_local_forces(
                    surface.calculate_forces(
                        local_velocity, angular_velocity))

        return surface_forces

    def calculate_thrust_forces(self):
        return None

    def calculate_weight_force(self, state):
        self.add_global_force("weight", state.position, self._weight)

    def weight(self):
        return self._weight
