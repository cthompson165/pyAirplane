from physics.vector_2d import Vector2D
from physics.angle import Angle
from flight.airplane import Airplane
from flight.engine import Engine
from flight.surface import Surface
from physics.state import State
from flight.atmosphere import Atmosphere
import flight.lift as lift
import flight.drag as drag


class SevenFourSeven(Airplane):

    MAX_ELEVATOR_DEGREES = 10

    def __init__(self, position, velocity):
        atmosphere = Atmosphere()

        state = State(position, velocity, Angle(0), 0)
        Airplane.__init__(self, state, self._mass(),
                          self._mass_moment_of_inertia(), atmosphere)

        wing_lift_curve = lift.Linear(6.98, 0.29, 5.5)
        wing_drag_curve = drag.LiftingLine(6.98, 0.0305, 0.75)
        self._wing = Surface("wing", Vector2D(0, 0), 0, Angle(2.4),
                             510.97, wing_lift_curve, wing_drag_curve,
                             atmosphere)

        stab_lift_curve = lift.LiftingLine(3.62)
        stab_drag_curve = drag.LiftingLine(3.62, efficiency_factor=0.6)
        self._horizontal_stabilizer = Surface(
            "stabilizer", Vector2D(-33, 0), 0, Angle(0), 136,
            stab_lift_curve, stab_drag_curve, atmosphere)

        fusilage_drag_curve = drag.Parasitic(0.27)
        # 747 cabin = ~19x6 meters
        self._fusilage = Surface("fusilage", self.cg(), 0, Angle(0), 118, None,
                                 fusilage_drag_curve, atmosphere)

        self._surfaces = []
        self._surfaces.append(self._wing)
        self._surfaces.append(self._horizontal_stabilizer)
        self._surfaces.append(self._fusilage)

        # don't have yaw forces (or a 3rd axis) to put engines out on wings
        # so they all go at cg
        self._engines = []
        self._engines.append(
            Engine("engine 1", self.cg(), Angle(0), 0, 275000))
        self._engines.append(
            Engine("engine 2", self.cg(), Angle(0), 0, 275000))
        self._engines.append(
            Engine("engine 3", self.cg(), Angle(0), 0, 275000))
        self._engines.append(
            Engine("engine 4", self.cg(), Angle(0), 0, 275000))

    def apply_pitch_control(self, percent):
        self._horizontal_stabilizer.angle = \
            Angle(SevenFourSeven.MAX_ELEVATOR_DEGREES * percent / 100.0)

    def _mass(self):
        return 289132.653061  # weight (F) / a (9.8)

    def _mass_moment_of_inertia(self):
        # length = 68.4
        # height = 19.4
        # radius = 4.5
        # cylinder
        # 1/12 * mass * length^2 + 1/4 * mass * radius^2
        return 112875928

    def surfaces(self):
        return self._surfaces

    def engines(self):
        return self._engines
