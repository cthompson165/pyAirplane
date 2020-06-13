from physics.vector_2d import Vector2D
import physics
import flight
import flight.drag as drag
import math


class Rock(flight.FlyingObject):
    def __init__(self, initial_pos, atmosphere):

        # setup physical properties
        radius = .05  # meters
        mass = 0.8384  # kg (rocks are 1600kg/m**3)
        area = math.pi * radius**2
        moment = 2/5 * mass * radius**2
        state = physics.State(position=initial_pos)
        flight.FlyingObject.__init__(self, mass, moment, state, atmosphere)

        # setup aerodynamic properties
        drag_curve = drag.Parasitic(drag.Parasitic.ShapeCoefficients.SPHERE)
        surface = flight.Surface(
            "rock", atmosphere=atmosphere, drag_curve=drag_curve, area=area)
        self._surfaces = [surface]

    # override flying_object methods needed for force calcs
    def surfaces(self):
        return self._surfaces


simulator = flight.Simulator()
atmosphere = flight.Atmosphere()
atmosphere.wind_speed = Vector2D(2, 0)  # add some wind to push off course
rock = Rock(Vector2D(0, 100), atmosphere)  # start at 100m
simulator.register_flying_object(rock)

time = 0
step_size = 1/30.0  # 1/30 second
while rock.position().y > 0:
    simulator.step(step_size)
    time += step_size
    print(str(round(time, 1)) + " seconds: " + str(round(rock.position(), 2)))
