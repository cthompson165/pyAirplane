from physics.vector_2d import Vector2D
import physics
import flight
import flight.drag as drag


class Rock:
    def __init__(self, initial_pos, atmosphere):

        # setup physical properties
        radius = 1
        mass = 1
        moment = 2/5 * mass * radius**2
        state = physics.State(atmosphere, position=initial_pos)
        physics.FlyingObject.__init__(self, mass, moment, state, atmosphere)

        # setup aerodynamic properties
        drag_curve = drag.Parasitic(drag.Parasitic.ShapeCoefficients.SPHERE)
        surface = flight.Surface(
            "rock", atmosphere=atmosphere, drag_curve=drag_curve)
        self._surfaces = (surface)

    def surfaces(self):
        ''' override flying_object "surfaces" method '''
        return self._surfaces


simulator = flight.Simulator()
atmosphere = flight.Atmosphere()
atmosphere.wind_speed = Vector2D(5, 0)
rock = Rock(Vector2D(0, 100), atmosphere)  # start at 100m
simulator.register_flying_object(rock)

while rock.position().y > 0:
    simulator.step(1/30.0)  # 1/30 second
    print("POS: " + str(rock.position()))
