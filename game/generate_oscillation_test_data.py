from aerodynamics.airplanes.seven_four_seven import SevenFourSeven
from aerodynamics.simulator import Simulator
from util.vector_2d import Vector2D


def run_sim():
    airplane = SevenFourSeven(Vector2D(0, 0),
                              Vector2D(265.3581764, 0))

    simulator = Simulator()
    simulator.register(airplane)
    t = 1.0/30

    # pitch up for 10 seconds
    airplane.apply_pitch_control(100)
    for i in range(0, 10):
        simulator.step(t)

    # neutral pitch to check oscillations
    airplane.apply_pitch_control(0)
    for i in range(0, 200):

        if i == 0 or i % 20 == 0:
            write(airplane)

        simulator.step(t)


def write(airplane):
    state = airplane.current_state()
    orientation = state.theta.degrees()
    precision = 8
    print("[" + str(round(orientation, precision)) + ", "
          + str(round(state.pos.x, precision)) + ", "
          + str(round(state.pos.y, precision)) + "],")


run_sim()
