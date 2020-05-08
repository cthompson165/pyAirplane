import unittest
from util.vector_2d import Vector2D
from aerodynamics.surface import Surface
from aerodynamics.lift_curves.linear_lift import LinearLift
from aerodynamics.lift_curves.lifting_line_lift import LiftingLineLift
from aerodynamics.drag_curves.lifting_line_drag import LiftingLineDrag
from util.angle import Angle


class TestSurface(unittest.TestCase):

    def get_surface(self, relative_degrees):
        return Surface("test", Vector2D(0, 0), relative_degrees, 0, None, None)

    def test_surface_aoa(self):
        surface = self.get_surface(0)
        aoa = surface.aoa(Angle(0), Vector2D(100, 0))
        self.assertAlmostEqual(0, aoa.relative_degrees())
    
    def test_surface_aoa_positive(self):
        surface = self.get_surface(0)
        aoa = surface.aoa(Angle(5), Vector2D(100, 0))
        self.assertAlmostEqual(5, aoa.relative_degrees())

    def test_surface_aoa_negative(self):
        surface = self.get_surface(0)
        aoa = surface.aoa(Angle(-5), Vector2D(100, 0))
        self.assertAlmostEqual(-5, aoa.relative_degrees())

    def test_surface_aoa_rotated(self):
        surface = self.get_surface(0)
        aoa = surface.aoa(Angle(47), Vector2D(100, 100))
        self.assertAlmostEqual(2, aoa.relative_degrees())

    def test_surface_aoa_rotated_huge_pos(self):
        surface = self.get_surface(0)
        aoa = surface.aoa(Angle(223), Vector2D(100, 100))
        self.assertAlmostEqual(178, aoa.relative_degrees())

    def test_surface_aoa_rotated_huge_neg(self):
        surface = self.get_surface(0)
        aoa = surface.aoa(Angle(227), Vector2D(100, 100))
        self.assertAlmostEqual(-178, aoa.relative_degrees())

    def test_surface_aoa_with_relative(self):
        surface = self.get_surface(3)
        aoa = surface.aoa(Angle(42), Vector2D(100, 100))
        self.assertAlmostEqual(0, aoa.relative_degrees())

    def test_surface_aoa_with_relative_positive(self):
        surface = self.get_surface(3)
        aoa = surface.aoa(Angle(45), Vector2D(100, 100))
        self.assertAlmostEqual(3, aoa.relative_degrees())
    
    def test_surface_aoa_with_relative_negative(self):
        surface = self.get_surface(3)
        aoa = surface.aoa(Angle(40), Vector2D(100, 100))
        self.assertAlmostEqual(-2, aoa.relative_degrees())

    ''' lift and drag '''
    # boeing examples from
    # http://www.aerospaceweb.org/question/aerodynamics/q0252.shtml

    # cessna from
    # http://www.aerospaceweb.org/question/aerodynamics/q0184.shtml

    def get_boeing_wing(self):
        wing_lift_curve = LinearLift(6.98, 0.29, 5.5)
        wing_drag_curve = LiftingLineDrag(6.98, 0.0305, 0.75)
        return Surface("boeing wing", Vector2D(0, 0), 2.4, 510.97, wing_lift_curve, wing_drag_curve)
 
    def get_cessna_wing(self): 
        
        wing_lift_curve = LiftingLineLift(7.37)
        wing_drag_curve = LiftingLineDrag(7.37, 0.027, 0.75)
        return Surface("cessna 172 wing", Vector2D(0, 0), 0, 16.2, wing_lift_curve, wing_drag_curve)

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
        self.assertAlmostEqual(661.93928, drag, 4, "0")

        drag = wing.calculate_drag(Angle(1), vel)
        self.assertAlmostEqual(672.44308, drag, 4, "1")

        drag = wing.calculate_drag(Angle(7), vel)
        self.assertAlmostEqual(1176.62500, drag, 4, "7")

# Some code to make the tests actually run.
if __name__ == '__main__':
    unittest.main()
