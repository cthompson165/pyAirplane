# pyAirplane
pyAirplane is a simple 2D flight dynamics engine in Python.

## Structure
Planes and kites start with `flight.flying_object`. Flying objects have one or more `flight.surface` objects that generate lift and drag based on the surface's `flight.lift_curve` and `flight drag_curve`. `flying_object` also takes care of collecting and applying the aerodynamic, thrust, and gravity forces acting on the object.

## Physics
The physics in the dynamics engine are generally pretty simple (forces and torques) so originally pyAirplane used a roll-your-own physics engine. But kites require a relatively more complex constraint force to simulate the kite string. I added pyMunk to provide the constraint forces and to replace the kinematic integration logic. pyMunk also provides resting contact forces which could be used to implement ground contact in the future. pyMunk is fully wrapped in the `flight.simulator` class so can be replaced with another engine if needed. 

The one thing pyMunk doesn't have that would be nice is a more accurate integrator like
runge kutta. Kites experience big forces relative to their mass so require more accurate integration
to avoid rocketing off into space. With euler integration the best we can do is use really small step sizes.

## Simple Example
Create a rock with drag and drop it from 100m (from examples/drop_a_rock.py):

Create the rock class and inherit from FlyingObject. It needs physical properties like weight and mass moment of inertia for gravity force calculation. Add a surface with parasitic drag for aerodynamic force calculation.
```
class Rock(flight.FlyingObject):
    def __init__(self, initial_pos, atmosphere):

        # setup physical properties
        radius = .05  # meters
        mass = 0.8384  # kg (rocks are 1600kg/m**3)
        area = math.pi * radius**2
        moment = 2/5 * mass * radius**2  # moment of a solid sphere
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
```

Then set up and run a simulation with a rock object.

```
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
```

The rock hits the ground after about 4.7 seconds and is blown off course by a little over .8 meters.

## Kite
fly_a_kite.py simulates flying a box kite. Use the left and right arrows to control the windspeed. 

For debugging forces, you can use the following keys:
* f: turn on and off graphical force display. Lift is show in blue, drag in light blue, velocity in green, and thrust in red.
* p: pause and unpause
* s: when paused, advance one step

## Airplane
fly_a_747.py simulates flying a 747 (with a bomber plane image because I am lazy). Use the up and down arrows to control the elevator and right and left to control thrust. If you have a flight-stick plugged in the simulation will try to use that. The airplane example implements the same debug keys as the kite example.

Note that the airplane will always explode if you try to land. Adding the ability to land would be a fun upgrade if anyone wants to take it on. You'd need to turn on collisions for stationary objects in `flight.simulator`, setup friction for wheels vs. any other part of the plane, and then determine how big a collision impulse a plane can experience without damage.

## Disclaimers
I wrote this for fun and don't guarantee the accuracy of any of it. I got a lot of the information from NASA's aerodynamics info website (https://www.grc.nasa.gov/WWW/K-12/airplane/short.html) so hopefully it is close. But please don't use it for anything important :-).
