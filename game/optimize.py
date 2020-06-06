from game.kite.box_kite import BoxKite
from util.vector_2d import Vector2D
from aerodynamics.simulator import Simulator
from physics.atmosphere import Atmosphere


kite = BoxKite(
    10, .7, .35, .175, .8, .55, Atmosphere(), Vector2D(0, 1000))

simulator = Simulator()
simulator.register_flying_object(kite)
t = 1/40.0
for i in range(0, 2000):
    simulator.step(t)
