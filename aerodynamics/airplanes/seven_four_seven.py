from util.vector_2d import Vector2D
from aerodynamics.airplane import Airplane
from aerodynamics.surface import Surface
from aerodynamics.lift_curves.linear_lift import LinearLift
from aerodynamics.lift_curves.lifting_line_lift import LiftingLineLift
from aerodynamics.drag_curves.lifting_line_drag import LiftingLineDrag


class SevenFourSeven(Airplane):

    MAX_ELEVATOR_DEGREES = 10

    def __init__(self, pos, vel):
        Airplane.__init__(self, pos, vel)

        wing_lift_curve = LinearLift(6.98, 0.29, 5.5)
        wing_drag_curve = LiftingLineDrag(6.98, 0.0305, 0.75)
        self._wing = Surface("wing", Vector2D(0, 0), 2.4,
                             510.97, wing_lift_curve, wing_drag_curve)

        stab_lift_curve = LiftingLineLift(3.62)
        stab_drag_curve = LiftingLineDrag(3.62)
        self._horizontal_stabilizer = Surface(
            "stabilizer", Vector2D(-33, 0), 0, 136,
            stab_lift_curve, stab_drag_curve)

        self._surfaces = []
        self._surfaces.append(self._wing)
        self._surfaces.append(self._horizontal_stabilizer)

    def apply_pitch_control(self, percent):
        self._horizontal_stabilizer.relative_degrees = \
            SevenFourSeven.MAX_ELEVATOR_DEGREES \
            * percent / 100.0

    def calculate_thrust(self, state):
        max_engine_thrust = 275000
        num_engines = 4
        max_total_thrust = max_engine_thrust * num_engines
        thrust_percent = 24
        orientation_unit = Vector2D(1, 0).rotate(state.theta)
        return orientation_unit.scale(max_total_thrust * thrust_percent / 100)

    def mass(self):
        return 289132.653061  # weight (F) / a (9.8)

    def mass_moment_of_inertia(self):
        # length = 68.4
        # height = 19.4
        # radius = 4.5
        # cylinder
        # 1/12 * mass * length^2 + 1/4 * mass * radius^2
        return 1000000  # 112875928

    def surfaces(self):
        return self._surfaces
