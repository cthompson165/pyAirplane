import unittest
from flight.atmosphere import Atmosphere


class TestAtmosphere(unittest.TestCase):

    def test_low(self):
        density = Atmosphere().get_air_density(500)
        self.assertEqual(1.225, density)

    def test_really_high(self):
        density = Atmosphere().get_air_density(100000)
        self.assertEqual(0.00001846, density)

    def test_really_low(self):
        density = Atmosphere().get_air_density(-10000)
        self.assertEqual(1.347, density)

    def test_exact_match(self):
        density = Atmosphere().get_air_density(5000)
        self.assertEqual(0.7364, density)

    def test_almost_next(self):
        density = Atmosphere().get_air_density(29999)
        self.assertEqual(0.04008, density)


# Some code to make the tests actually run.
if __name__ == '__main__':
    unittest.main()
