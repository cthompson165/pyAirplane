import unittest
from util.vector2d import Vector2D
from aerodynamics.surface import Surface
from aerodynamics.surfaces.thinAirfoil import ThinAirfoil
from util.angle import Angle


class TestSurface(unittest.TestCase):

    def get_surface(self, relativeDegrees):
        return Surface("test", Vector2D(0, 0), relativeDegrees, 0)

    def test_surface_aoa(self):
        surface = self.get_surface(0)
        aoa = surface.AoA(Angle(0), Vector2D(100, 0))
        self.assertAlmostEqual(0, aoa.relativeDegrees())
    
    def test_surface_aoa_positive(self):
        surface = self.get_surface(0)
        aoa = surface.AoA(Angle(5), Vector2D(100, 0))
        self.assertAlmostEqual(5, aoa.relativeDegrees())

    def test_surface_aoa_negative(self):
        surface = self.get_surface(0)
        aoa = surface.AoA(Angle(-5), Vector2D(100, 0))
        self.assertAlmostEqual(-5, aoa.relativeDegrees())

    def test_surface_aoa_rotated(self):
        surface = self.get_surface(0)
        aoa = surface.AoA(Angle(47), Vector2D(100, 100))
        self.assertAlmostEqual(2, aoa.relativeDegrees())

    def test_surface_aoa_rotated_huge_pos(self):
        surface = self.get_surface(0)
        aoa = surface.AoA(Angle(223), Vector2D(100, 100))
        self.assertAlmostEqual(178, aoa.relativeDegrees())

    def test_surface_aoa_rotated_huge_neg(self):
        surface = self.get_surface(0)
        aoa = surface.AoA(Angle(227), Vector2D(100, 100))
        self.assertAlmostEqual(-178, aoa.relativeDegrees())

    def test_surface_aoa_with_relative(self):
        surface = self.get_surface(3)
        aoa = surface.AoA(Angle(42), Vector2D(100, 100))
        self.assertAlmostEqual(0, aoa.relativeDegrees())

    def test_surface_aoa_with_relative_positive(self):
        surface = self.get_surface(3)
        aoa = surface.AoA(Angle(45), Vector2D(100, 100))
        self.assertAlmostEqual(3, aoa.relativeDegrees())
    
    def test_surface_aoa_with_relative_negative(self):
        surface = self.get_surface(3)
        aoa = surface.AoA(Angle(40), Vector2D(100, 100))
        self.assertAlmostEqual(-2, aoa.relativeDegrees())

    ''' lift and drag '''
    # boeing examples from
    # http://www.aerospaceweb.org/question/aerodynamics/q0252.shtml

    # cessna from
    # http://www.aerospaceweb.org/question/aerodynamics/q0184.shtml

    def get_boeing_wing(self):
        return ThinAirfoil("boeing wing", Vector2D(0, 0), 2.4, 510.97, 6.98, 5.5, 0.29, 0.0305, 0.75)

    def get_cessna_wing(self):
        return ThinAirfoil("cessna 172 wing", Vector2D(0, 0), 0, 16.2, 7.37, 0, 0, 0.027, 0.75)

    def test_boeing_lift(self):

        vel = Vector2D(265.5, 0)
        lift = self.get_boeing_wing().calculate_lift(Angle(0), vel)
        self.assertEqual(2836530, round(lift, 0))

    def test_cessna_lift(self):

        vel = Vector2D(100, 0)
        wing = self.get_cessna_wing()

        lift = wing.calculate_lift(Angle(0), vel)
        self.assertAlmostEqual(0, lift, 4, "0")

        lift = wing.calculate_lift(Angle(1), vel)
        self.assertAlmostEqual(2114.655024, lift, 4, "1")

        lift = wing.calculate_lift(Angle(7), vel)
        self.assertAlmostEqual(14802.58517, lift, 4, "7")

    def test_cessna_drag(self):

        vel = Vector2D(100, 0)
        wing = self.get_cessna_wing()

        drag = wing.calculate_drag(Angle(0), vel)
        self.assertAlmostEqual(661.93929, drag, 4, "0")

        drag = wing.calculate_drag(Angle(1), vel)
        self.assertAlmostEqual(672.4430802, drag, 4, "1")

        drag = wing.calculate_drag(Angle(7), vel)
        self.assertAlmostEqual(1176.625008, drag, 4, "7")

# Some code to make the tests actually run.
if __name__ == '__main__':
    unittest.main()
