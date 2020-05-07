from aerodynamics.airplanes.sevenFourSeven import SevenFourSeven
from util.vector2d import Vector2D

def runSim(steps):
    airplane = SevenFourSeven(Vector2D(0, 0),
               Vector2D(265.3581764, 0))

    t = 1.0/30
    time = 0

    f = open("../out.csv", "w")
    airplane.apply_pitch_control(100)
    for i in range(0, 10):
      airplane.step(t)

    airplane.apply_pitch_control(0)
    for i in range(0, steps):
        f.write(str(time) + "," + str(AdjustAngle(airplane.state.theta)) + "\n")
        airplane.step(t)
        time += t

    f.close()

def AdjustAngle(angle):
    if angle.degrees() < 300:
        return angle.degrees() + 360
    else:
        return angle.degrees()


runSim(200)
print("done")