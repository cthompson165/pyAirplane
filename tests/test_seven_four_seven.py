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

        expected = [359.15770786089723, 88.3260962917008, 0.15924856394764386]
        actual = actuals[0]
        self.run_test(actual, expected)

        expected = [356.18048407279366,
                    264.2500441732677, -0.10456317247022187]
        actual = actuals[20]
        self.run_test(actual, expected)

        expected = [355.4821708735367, 439.32124573927024, -3.277970413590195]
        actual = actuals[40]
        self.run_test(actual, expected)

        expected = [356.91781024517104, 613.5795649633196, -9.20931833529732]
        actual = actuals[60]
        self.run_test(actual, expected)

        expected = [359.0576642323963, 787.0634324136869, -16.137307502303603]
        actual = actuals[80]
        self.run_test(actual, expected)

        expected = [360.39288393239275, 959.7517046853794, -22.20637260594219]
        actual = actuals[100]
        self.run_test(actual, expected)

        expected = [360.2731314364735, 1131.5815439074154, -26.6456670564564]
        actual = actuals[120]
        self.run_test(actual, expected)

        expected = [359.07658000769356,
                    1302.5364564757956, -29.977348409802495]
        actual = actuals[140]
        self.run_test(actual, expected)

        expected = [357.71827921872017, 1472.6574244571432, -33.39182465905179]
        actual = actuals[160]
        self.run_test(actual, expected)

        expected = [356.9728763676182, 1641.9933428910135, -37.89605797259146]
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
