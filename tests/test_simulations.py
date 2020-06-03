import unittest
from util.vector_2d import Vector2D
from aerodynamics.simulator import Simulator
from game.kite.box_kite import BoxKite
from aerodynamics.airplanes.seven_four_seven import SevenFourSeven


class TestSimulations(unittest.TestCase):

    def test_free_fall(self):

        expected_data = \
            [[70.0, 0.0, 1000.0],
             [40.4921178, -6.65173639, 989.09038239],
                [15.91822377, -17.06629591, 983.19585049],
                [358.91187172, -20.31526146, 979.20775524],
                [359.99181078, -20.24047453, 974.22071749],
                [0.00143368, -20.24039081, 969.23108851],
                [359.99994132, -20.24046779, 964.24146648],
                [1.33e-06, -20.24046429, 959.25184208],
                [360.0, -20.24046438, 954.26221778],
                [360.0, -20.24046438, 949.27259348],
                [0.0, -20.24046438, 944.28296917],
                [360.0, -20.24046438, 939.29334487],
                [0.0, -20.24046438, 934.30372057],
                [0.0, -20.24046438, 929.31409626],
                [0.0, -20.24046438, 924.32447196],
                [0.0, -20.24046438, 919.33484766],
                [0.0, -20.24046438, 914.34522336],
                [0.0, -20.24046438, 909.35559905],
                [360.0, -20.24046438, 904.36597475],
                [360.0, -20.24046438, 899.37635045]]

        self.run_tests(self.get_box_kite_data(), expected_data)

    def test_747_oscillations(self):

        expected_data = \
            [[359.17347137, 88.32620481, 0.1561356],
             [356.48284628, 264.25019804, -0.13188468],
                [356.09247044, 439.32030925, -3.1201515],
                [357.43076867, 613.57672006, -8.43885686],
                [359.07341657, 787.04485478, -14.48941592],
                [359.90204006, 959.70291679, -19.86433778],
                [359.66463985, 1131.51310978, -24.14517915],
                [358.81848552, 1302.47375829, -27.82272983],
                [358.01115577, 1472.61538864, -31.70820811],
                [357.63739893, 1641.97269083, -36.36946191]]

        self.run_tests(self.get_747_data(), expected_data)

    def run_tests(self, actual_data, expected_data):
        expected_index = 0
        for actual in actual_data:
            expected = expected_data[expected_index]
            expected_index += 1
            self.run_test(actual, expected)

    def run_test(self, actual, expected):
        self.assertAlmostEqual(expected[0], actual[0], 7)
        self.assertAlmostEqual(expected[1], actual[1], 7)
        self.assertAlmostEqual(expected[2], actual[2], 7)

    def get_box_kite_data(self):

        kite = BoxKite(
            10, .7, .35, .175, .8, .55, Vector2D(0, 1000))

        simulator = Simulator()
        simulator.register(kite)
        steps = 2000
        step_size = 100

        t = 1/30.0
        actual_data = []
        for i in range(0, steps):
            simulator.step(t)
            state = kite.current_state()

            if i == 0 or i % step_size == 0:
                actual = [state.theta.degrees(),
                          state.pos.x, state.pos.y]
                actual_data.append(actual)

        return actual_data

    def get_747_data(self):

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

        steps = 200
        step_size = 20

        t = 1/30.0
        actual_data = []
        for i in range(0, steps):
            state = airplane.current_state()

            if i == 0 or i % step_size == 0:
                actual = [state.theta.degrees(),
                          state.pos.x, state.pos.y]
                actual_data.append(actual)

            simulator.step(t)

        return actual_data


# Some code to make the tests actually run.
if __name__ == '__main__':
    unittest.main()
