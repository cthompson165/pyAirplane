import unittest
from util.vector_2d import Vector2D
from util.angle import Angle
from physics.force import Force
from aerodynamics.surface import Surface
from aerodynamics.lift_curves.linear_lift import LinearLift
from aerodynamics.lift_curves.lifting_line_lift import LiftingLineLift
from aerodynamics.drag_curves.lifting_line_drag import LiftingLineDrag


class TestSurface(unittest.TestCase):

    def get_surface(self, relative_degrees):
        return Surface("test", Vector2D(0, 0), Angle(relative_degrees),
                       10, None, None)

    def test_surface_aoa(self):
        surface = self.get_surface(0)
        aoa = surface.aoa(Vector2D(100, 0))
        self.assertAlmostEqual(0, aoa.relative_degrees())

    def test_surface_aoa_positive(self):
        surface = self.get_surface(0)
        aoa = surface.aoa(Vector2D(100, -8.75))
        self.assertAlmostEqual(5, aoa.relative_degrees(), 2)

    def test_surface_aoa_negative(self):
        surface = self.get_surface(0)
        aoa = surface.aoa(Vector2D(100, 8.75))
        self.assertAlmostEqual(-5, aoa.relative_degrees(), 2)

    def test_surface_aoa_rotated_huge_pos(self):
        surface = self.get_surface(0)
        aoa = surface.aoa(Vector2D(-100, -3.49))
        self.assertAlmostEqual(178, aoa.relative_degrees(), 2)

    def test_surface_aoa_rotated_huge_neg(self):
        surface = self.get_surface(0)
        aoa = surface.aoa(Vector2D(-100, 3.49))
        self.assertAlmostEqual(-178, aoa.relative_degrees(), 2)

    # lift and drag
    # boeing examples from
    # http://www.aerospaceweb.org/question/aerodynamics/q0252.shtml

    # cessna from
    # http://www.aerospaceweb.org/question/aerodynamics/q0184.shtml

    def get_boeing_wing(self):
        wing_lift_curve = LinearLift(6.98, 0.29, 5.5)
        wing_drag_curve = LiftingLineDrag(6.98, 0.0305, 0.75)
        return Surface(
            "boeing wing", Vector2D(0, 0), Angle(2.4), 510.97,
            wing_lift_curve, wing_drag_curve)

    def get_cessna_wing(self):

        wing_lift_curve = LiftingLineLift(7.37)
        wing_drag_curve = LiftingLineDrag(7.37, 0.027, 0.75)
        return Surface(
            "cessna 172 wing", Vector2D(0, 0), Angle(0), 16.2,
            wing_lift_curve, wing_drag_curve)

    def get_lift(self, velocity, surface, angle):

        forces = surface.calculate_forces(velocity.rotate(angle), 0)
        lift = [force for force in forces if force.source == Force.Source.lift]
        if len(lift) == 1:
            return lift[0].vector.magnitude()
        else:
            return None

    def get_drag(self, velocity, surface, angle):

        forces = surface.calculate_forces(velocity.rotate(angle), 0)
        drag = [force for force in forces if force.source == Force.Source.drag]
        if len(drag) == 1:
            return drag[0].vector.magnitude()
        else:
            return None

    def test_boeing_lift(self):

        velocity = Vector2D(265.5, 0)
        surface = self.get_boeing_wing()
        lift = self.get_lift(velocity, surface, Angle(0))

        self.assertAlmostEqual(2836530, lift, 0)

    def test_cessna_lift(self):

        velocity = Vector2D(100, 0)
        wing = self.get_cessna_wing()

        lift = self.get_lift(velocity, wing, Angle(0))
        self.assertAlmostEqual(0, lift, 4, "0")

        lift = self.get_lift(velocity, wing, Angle(1))
        self.assertAlmostEqual(2114.655024, lift, 4, "1")

        lift = self.get_lift(velocity, wing, Angle(7))
        self.assertAlmostEqual(14802.58517, lift, 4, "7")

    def test_cessna_drag(self):

        velocity = Vector2D(100, 0)
        wing = self.get_cessna_wing()

        drag = self.get_drag(velocity, wing, Angle(0))
        self.assertAlmostEqual(661.93928, drag, 4, "0")

        drag = self.get_drag(velocity, wing, Angle(1))
        self.assertAlmostEqual(672.44308, drag, 4, "1")

        drag = self.get_drag(velocity, wing, Angle(7))
        self.assertAlmostEqual(1176.62500, drag, 4, "7")


# Some code to make the tests actually run.
if __name__ == '__main__':
    unittest.main()
