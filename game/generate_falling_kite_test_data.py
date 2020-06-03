from game.kite.box_kite import BoxKite
from util.vector_2d import Vector2D
from aerodynamics.simulator import Simulator


def run_sim():
    kite = BoxKite(
        10, .7, .35, .175, .8, .55, Vector2D(0, 1000))

    simulator = Simulator()
    simulator.register(kite)
    t = 1/30.0
    for i in range(0, 2000):
        simulator.step(t)
        if i == 0 or i % 100 == 0:
            write(kite)


def write(kite):
    state = kite.current_state()
    orientation = state.theta.degrees()
    precision = 8
    print("[" + str(round(orientation, precision)) + ", "
          + str(round(state.pos.x, precision)) + ", "
          + str(round(state.pos.y, precision)) + "],")


run_sim()
