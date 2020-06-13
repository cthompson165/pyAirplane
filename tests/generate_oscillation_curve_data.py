from aerodynamics.airplanes.seven_four_seven import SevenFourSeven
from aerodynamics.simulator import Simulator
from physics.vector_2d import Vector2D

orientations = []
success = True


def run_sim(steps):
    airplane = SevenFourSeven(Vector2D(0, 14000),
                              Vector2D(265.3581764, 0))
    simulator = Simulator()
    simulator.register_flying_object(airplane)

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
    orientation = adjust_angle(airplane.orientation())
    position = airplane.position()

    # original curve was made at sea level y pos but at 
    # 747 cruising altitude air density. subtract 14K
    # to get the two to match up
    f.write(
        str(time) + ","
        + str(orientation) + ","
        + str(position.x) + ","
        + str(position.y - 14000)
        + "\n")

    orientations.append(orientation)


def adjust_angle(angle):
    if angle.degrees() < 300:
        return angle.degrees() + 360
    else:
        return angle.degrees()


print("generating curve data...")
run_sim(200)
print("done")
