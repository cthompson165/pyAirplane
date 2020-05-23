class RigidBody:
    ''' Calculates state based on forces '''

    # Vector2D pos and vel. theta in degrees
    def __init__(self, mass, mass_moment_of_inertia, state):
        self._state = state
        self._mass = mass
        self._mass_moment_of_inertia = mass_moment_of_inertia

    def mass(self):
        return self._mass

    def pos(self):
        return self._state.pos.copy()

    def orientation(self):
        return self._state.theta

    def current_state(self):
        return self._state.copy()

    def calculate_forces(self, state):
        raise NotImplementedError()

    @staticmethod
    def get_local_velocity(state):
        return state.vel.rotate(state.theta.times_constant(-1))
