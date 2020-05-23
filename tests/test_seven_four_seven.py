import unittest
from util.vector_2d import Vector2D
from aerodynamics.simulator import Simulator
from aerodynamics.airplanes.seven_four_seven import SevenFourSeven


class TestSevenFourSeven(unittest.TestCase):

    def test_forces_balance(self):
        vel = Vector2D(265.3581764, 0)
        pos = Vector2D(200, 200)
        airplane = SevenFourSeven(pos, vel)
        simulator = Simulator()
        simulator.register(airplane)

        simulator.step(1)
        self.assertEqual(0, round(airplane.current_state().vel.y, 2))

    def test_weight(self):
        airplane = SevenFourSeven(Vector2D(200, 200), Vector2D(265.3581764, 0))
        self.assertEqual(2833500, round(airplane.weight().magnitude(), 3))

    def test_oscillation(self):
        airplane = SevenFourSeven(Vector2D(0, 0),
                                  Vector2D(265.3581764, 0))

        simulator = Simulator()
        simulator.register(airplane)

        t = 1.0/30
        time = 0

        # pitch up for 10 seconds
        airplane.apply_pitch_control(100)
        for i in range(0, 10):
            simulator.step(t)
            time += t

        orientations = []

        # neutral pitch to check oscillations
        airplane.apply_pitch_control(0)
        for i in range(0, 200):
            orientation = self.adjust_angle(airplane.current_state().theta)
            orientations.append(orientation)
            simulator.step(t)
            time += t

        self.assertAlmostEqual(orientations[0], 358.4155297)
        self.assertAlmostEqual(orientations[9], 355.9076582)
        self.assertAlmostEqual(orientations[36], 356.1167718)
        self.assertAlmostEqual(orientations[82], 360.4672736)
        self.assertAlmostEqual(orientations[123], 357.4159406)
        self.assertAlmostEqual(orientations[189], 358.6308471)
        self.assertAlmostEqual(orientations[199], 358.3319444)

    def adjust_angle(self, angle):
        if angle.degrees() < 300:
            return angle.degrees() + 360
        else:
            return angle.degrees()


# Some code to make the tests actually run.
if __name__ == '__main__':
    unittest.main()
