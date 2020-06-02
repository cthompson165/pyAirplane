import unittest
from util.vector_2d import Vector2D
from aerodynamics.simulator import Simulator
from aerodynamics.airplanes.seven_four_seven import SevenFourSeven


class TestSevenFourSeven(unittest.TestCase):

    def test_forces_balance(self):
        velocity = Vector2D(265.3581764, 0)
        pos = Vector2D(200, 200)
        airplane = SevenFourSeven(pos, velocity)
        simulator = Simulator()
        simulator.register(airplane)

        simulator.step(1)
        self.assertEqual(0, round(airplane.current_state().airspeed().y, 2))

    def test_weight(self):
        airplane = SevenFourSeven(Vector2D(200, 200), Vector2D(265.3581764, 0))
        self.assertEqual(2833500, round(airplane.weight().magnitude(), 3))

    def test_oscillation(self):
        airplane = SevenFourSeven(Vector2D(0, 0),
                                  Vector2D(265.3581764, 0))

        simulator = Simulator()
        simulator.register(airplane)

        t = 1.0/30

        # pitch up for 10 seconds
        airplane.apply_pitch_control(100)
        for i in range(0, 10):
            simulator.step(t)

        actuals = []

        # neutral pitch to check oscillations
        airplane.apply_pitch_control(0)
        for i in range(0, 200):
            state = airplane.current_state()
            actuals.append(
                [self.adjust_angle(state.theta), state.pos.x, state.pos.y])
            simulator.step(t)

        expected = [359.1734832, 88.3262049, 0.156133215]
        actual = actuals[0]
        self.run_test(actual, expected)

        expected = [356.4833968, 264.2501987, -0.131940265]
        actual = actuals[20]
        self.run_test(actual, expected)

        expected = [356.0934039, 439.3203082, -3.119856627]
        actual = actuals[40]
        self.run_test(actual, expected)

        expected = [357.4315431, 613.5767113, -8.437581475]
        actual = actuals[60]
        self.run_test(actual, expected)

        expected = [359.0736694, 787.0448122, -14.48680516]
        actual = actuals[80]
        self.run_test(actual, expected)

        expected = [359.9018635, 959.702809, -19.86053268]
        actual = actuals[100]
        self.run_test(actual, expected)

        expected = [359.6644, 1131.512925, -24.14061808]
        actual = actuals[120]
        self.run_test(actual, expected)

        expected = [358.8184732, 1302.473496, -27.81778772]
        actual = actuals[140]
        self.run_test(actual, expected)

        expected = [358.0114411, 1472.615047, -31.70299646]
        actual = actuals[160]
        self.run_test(actual, expected)

        expected = [357.637848, 1641.972261, -36.36384464]
        actual = actuals[180]
        self.run_test(actual, expected)

    def run_test(self, actual, expected):
        self.assertAlmostEqual(expected[0], actual[0], 6)
        self.assertAlmostEqual(expected[1], actual[1], 6)
        self.assertAlmostEqual(expected[2], actual[2], 6)

    def adjust_angle(self, angle):
        if angle.degrees() < 300:
            return angle.degrees() + 360
        else:
            return angle.degrees()


# Some code to make the tests actually run.
if __name__ == '__main__':
    unittest.main()
