from aerodynamics.kites.box_kite import BoxKite
from physics.vector_2d import Vector2D
from aerodynamics.simulator import Simulator
from physics.atmosphere import Atmosphere


kite = BoxKite(
    .7, .35, .175, Atmosphere(),
    initial_pos=Vector2D(0, 1000))

simulator = Simulator()
simulator.register_flying_object(kite)
t = 1/40.0
print("start")
for i in range(0, 2000):
    simulator.step(t)
print("done")
