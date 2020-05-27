from util.angle import Angle
from util.vector_2d import Vector2D
from physics.state import State
from physics.force import Force
from aerodynamics.airplane import Airplane


class SimplePlane(Airplane):
    def __init__(self, pos, velocity):
        state = State(pos, velocity, Angle(0), 0)
        Airplane.__init__(self, state, self._mass(),
                          self._mass_moment_of_inertia())

    def apply_pitch_control(self, percent):
        pass

    def get_force_vectors(self, velocity):
        raise NotImplementedError()

    def calculate_forces(self, state, atmosphere):
        force_vectors = self.get_force_vectors(self._mass, state.airspeed())
        forces = []
        for force_vector in force_vectors:
            forces.append(Force(
                Force.Source.other, "any",
                self.cg().add(Vector2D(-40, 0)),
                force_vector))

        return forces

    def _mass(self):
        return 289133

    def _mass_moment_of_inertia(self):
        return 10000

    def surfaces(self):
        return None

    def engines(self):
        return None
