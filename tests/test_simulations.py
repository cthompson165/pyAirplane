import unittest
from physics.vector_2d import Vector2D
from flight.simulator import Simulator
from flight.kites.box_kite import BoxKite
from flight.planes.seven_four_seven import SevenFourSeven
from flight.atmosphere import Atmosphere
from flight.kites.bridle import Bridle


class TestSimulations(unittest.TestCase):

    def test_free_fall(self):

        expected_data = \
            [[70.0, 0.0, 14000.0],
             [40.4921178, -6.65173639, 13989.09038239],
                [15.91822377, -17.06629591, 13983.19585049],
                [358.91187172, -20.31526146, 13979.20775524],
                [359.99181078, -20.24047453, 13974.22071749],
                [0.00143368, -20.24039081, 13969.23108851],
                [359.99994132, -20.24046779, 13964.24146648],
                [1.33e-06, -20.24046429, 13959.25184208],
                [360.0, -20.24046438, 13954.26221778],
                [360.0, -20.24046438, 13949.27259348],
                [0.0, -20.24046438, 13944.28296917],
                [360.0, -20.24046438, 13939.29334487],
                [0.0, -20.24046438, 13934.30372057],
                [360.0, -20.24046438, 13929.31409626],
                [360.0, -20.24046438, 13924.32447196],
                [360.0, -20.24046438, 13919.33484766],
                [0.0, -20.24046438, 13914.34522336],
                [0.0, -20.24046438, 13909.35559905],
                [0.0, -20.24046438, 13904.36597475],
                [0.0, -20.24046438, 13899.37635045]]

        self.run_tests(self.get_box_kite_data(), expected_data)

    def test_747_oscillations(self):

        expected_data = \
            [[359.17347137, 88.32620481, 14000.1561356],
             [356.48284628, 264.25019804, 13999.86811532],
                [356.09247044, 439.32030925, 13996.8798485],
                [357.43076867, 613.57672006, 13991.56114314],
                [359.07341657, 787.04485478, 13985.51058408],
                [359.90204006, 959.70291679, 13980.13566222],
                [359.66463985, 1131.51310978, 13975.85482085],
                [358.81848552, 1302.47375829, 13972.17727017],
                [358.01115577, 1472.61538864, 13968.29179189],
                [357.63739893, 1641.97269083, 13963.63053809]]

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

        kite = BoxKite(.7, .35, .175, Atmosphere(),
                       initial_pos=Vector2D(0, 14000))

        simulator = Simulator()
        simulator.register_flying_object(kite)
        steps = 2000
        step_size = 100

        t = 1/30.0
        actual_data = []
        for i in range(0, steps):
            simulator.step(t)
            position = kite.position()

            if i == 0 or i % step_size == 0:
                actual = [kite.orientation().degrees(),
                          position.x, position.y]
                actual_data.append(actual)

        return actual_data

    def get_747_data(self):

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

        steps = 200
        step_size = 20

        t = 1/30.0
        actual_data = []
        for i in range(0, steps):
            if i == 0 or i % step_size == 0:
                position = airplane.position()
                actual = [airplane.orientation().degrees(),
                          position.x, position.y]
                actual_data.append(actual)

            simulator.step(t)

        return actual_data


# Some code to make the tests actually run.
if __name__ == '__main__':
    unittest.main()
