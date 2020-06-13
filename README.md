# pyAirplane
pyAirplane is a simple 2D flight dynamics engine.

## Structure
Planes and kites start with flight.flying_object. flying_objects have surfaces that generate
lift and drag based on the surface's lift and drag curves. flying_object also takes care of 
collecting and applying the aerodynamic, thrust, and gravity forces acting on a flying object.

## Physics
The physics in the dynamics engine are generally pretty simple (forces and torques) so originally 
pyAirplane used a custom physics engine. But kites require constraint forces which are a lot more
complex. I added pyMunk to provide the constraint forces and to replace the custom kinematic integration
logic. pyMunk also provides resting contact forces which could be used to implement ground contact
in the future. pyMunk is fully wrapped in the flight.simulator class so can be replaced with another engine
if needed. 

The one thing pyMunk doesn't have that would be nice is a more accurate integrator like
runge kutta. Kites experience big forces relative to their mass so require more accurate integration
to avoid rocketing off into space. With euler integration the best we can do is use really small step 
sizes.

##