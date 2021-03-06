import unittest
from physics.vector_2d import Vector2D
from flight.kites.box_kite import BoxKite
from flight.planes.seven_four_seven import SevenFourSeven
import flight


class TestSimulations(unittest.TestCase):

    def test_free_fall(self):

        expected_data = \
            [[70.0, 0.0, 14000.0],
             [61.71648348, -3.4273445, 13989.10792986],
                [27.85971874, -11.12015789, 13981.21864443],
                [354.3591102, -17.78694256, 13977.21943405],
                [0.24438141, -17.45351158, 13972.25328197],
                [0.02134659, -17.47071505, 13967.26444635],
                [359.99791294, -17.47195259, 13962.27485652],
                [359.99995777, -17.47181501, 13957.28522872],
                [1.286e-05, -17.47181315, 13952.29560436],
                [359.99999977, -17.47181397, 13947.30598008],
                [359.99999994, -17.47181395, 13942.31635577],
                [0.0, -17.47181395, 13937.32673147],
                [0.0, -17.47181395, 13932.33710717],
                [360.0, -17.47181395, 13927.34748286],
                [360.0, -17.47181395, 13922.35785856],
                [0.0, -17.47181395, 13917.36823426],
                [0.0, -17.47181395, 13912.37860995],
                [0.0, -17.47181395, 13907.38898565],
                [360.0, -17.47181395, 13902.39936135],
                [360.0, -17.47181395, 13897.40973705]]

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

        kite = BoxKite(.7, .35, .175, flight.Atmosphere(),
                       initial_pos=Vector2D(0, 14000))

        simulator = flight.Simulator()
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

        simulator = flight.Simulator()
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
