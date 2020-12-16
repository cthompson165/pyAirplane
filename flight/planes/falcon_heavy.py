from physics.vector_2d import Vector2D
from flight.airplane import Airplane
import physics
from physics.angle import Angle
import flight
import flight.drag as drag
from flight.surface import Surface
from flight.engine import Engine
import flight.lift as lift
import math


class FalconHeavy(Airplane):
    def __init__(self, initial_pos, initial_vel, atmosphere):

        # setup physical properties
        radius = 3.66 / 2  # meters

        # ignore the side boosters for now - and use fins with a drag and lift
        # curve
        area = math.pi * radius**2

        # I'm not sure about these numbers. Not sure why thrust is ~20x weight
        # fully loaded. For now set throttle to 5 or 6% to get realistic
        # acceleration
        mass = 1420000 / 9.8  # kg
        thrust = 22241102  # N

        length = 70  # m
        # cylinder
        # 1/12 * mass * length^2 + 1/4 * mass * radius^2
        moment = 1/12 * mass * length**2 + 1/4 * mass * radius**2

        state = physics.State(position=initial_pos, velocity=initial_vel,
                              orientation=Angle(90))
        Airplane.__init__(self, state, mass,
                          moment, atmosphere)

        # setup aerodynamic properties
        drag_curve = drag.Parasitic(.35)
        surface = flight.Surface(
            "rocket", atmosphere=atmosphere, drag_curve=drag_curve, area=area)

        stab_lift_curve = lift.LiftingLine(3.62)
        stab_drag_curve = drag.LiftingLine(3.62, efficiency_factor=0.6)
        stab = Surface(
            "stabilizer", Vector2D(-33, 0), 0, Angle(0), 136,
            stab_lift_curve, stab_drag_curve, atmosphere)

        self._surfaces = [surface, stab]

        engine = Engine("1d merlin", Vector2D(-21, 0), Angle(0), 0, thrust)
        engine.set_throttle(100)
        self._engines = [engine]

    # override flying_object methods needed for force calcs
    def surfaces(self):
        return self._surfaces

    def engines(self):
        return self._engines

    def apply_pitch_control(self, percent):
        pass
