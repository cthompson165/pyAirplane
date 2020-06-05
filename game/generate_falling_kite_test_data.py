from game.kite.box_kite import BoxKite
from util.vector_2d import Vector2D
from aerodynamics.simulator import Simulator


def run_sim():
    kite = BoxKite(
        10, .7, .35, .175, .8, .55, Vector2D(0, 1000))

    simulator = Simulator()
    simulator.register_flying_object(kite)
    t = 1/30.0
    for i in range(0, 2000):
        simulator.step(t)
        if i == 0 or i % 100 == 0:
            write(kite)


def write(kite):
    orientation = kite.orientation().degrees()
    precision = 8
    position = kite.pos()
    print("[" + str(round(orientation, precision)) + ", "
          + str(round(position.x, precision)) + ", "
          + str(round(position.y, precision)) + "],")


run_sim()
