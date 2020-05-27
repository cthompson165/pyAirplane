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

    def calculate_forces(self, state, atmosphere):
        raise NotImplementedError()

    @staticmethod
    def get_local_airspeed(state):
        return state.airspeed().rotate(state.theta.times_constant(-1))
