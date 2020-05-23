import sys
from aerodynamics.airplanes.seven_four_seven import SevenFourSeven
from aerodynamics.simulator import Simulator
from util.vector_2d import Vector2D

orientations = []
success = True


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


def check(index, expected):
    global success
    actual = orientations[index]
    if round(expected, 5) != round(actual, 5):
        print("Not equal " + str(index))
        success = False


def write(time, airplane, f):
    orientation = adjust_angle(airplane.current_state().theta)
    f.write(
        str(time) + ","
        + str(orientation) + "\n")

    orientations.append(orientation)


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

# check some results

check(0, 358.4155297)
check(9, 355.9076582)
check(36, 356.1167718)
check(82, 360.4672736)
check(123, 357.4159406)
check(189, 358.6308471)
check(199, 358.3319444)

if success:
    print("Checked out")
