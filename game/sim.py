import sys
from aerodynamics.airplanes.seven_four_seven import SevenFourSeven
from util.vector_2d import Vector2D
from physics.simulator import Simulator


def run_sim(steps):
    airplane = SevenFourSeven(Vector2D(0, 0),
                              Vector2D(265.3581764, 0))

    simulator = Simulator()
    simulator.register(airplane)

    t = 1.0/30
    time = 0

    f = open("../doc/out.csv", "w")

    # pitch up for 10 seconds
    airplane.apply_pitch_control(100)
    for i in range(0, 10):
        simulator.step(t)
        time += t

    # neutral pitch to check oscillations
    airplane.apply_pitch_control(0)
    for i in range(0, steps):
        write(time, airplane, f)
        simulator.step(t)
        time += t

    f.close()


def write(time, airplane, f):
    f.write(
        str(time) + ","
        + str(adjust_angle(airplane.current_state().theta)) + "\n")


def adjust_angle(angle):
    if angle.degrees() < 300:
        return angle.degrees() + 360
    else:
        return angle.degrees()


steps = 200
if len(sys.argv) > 1:
    steps = int(sys.argv[1])

print("running for " + str(steps) + " steps")
run_sim(steps)
print("done")
