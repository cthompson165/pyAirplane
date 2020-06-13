from flight.planes.seven_four_seven import SevenFourSeven
from flight.simulator import Simulator
from physics.vector_2d import Vector2D


def run_sim():
    airplane = SevenFourSeven(Vector2D(0, 14000),
                              Vector2D(265.3581764, 0))

    simulator = Simulator()
    simulator.register_flying_object(airplane)
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
    orientation = airplane.orientation().degrees()
    precision = 8
    position = airplane.position()
    print("[" + str(round(orientation, precision)) + ", "
          + str(round(position.x, precision)) + ", "
          + str(round(position.y, precision)) + "],")


run_sim()
