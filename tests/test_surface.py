import unittest
from physics.vector_2d import Vector2D
from physics.angle import Angle
from physics.state import State
from physics.atmosphere import Atmosphere
from flight.simulator import Simulator
from flight.surface import Surface
from flight.lift.linear_lift import LinearLift
from flight.lift.lifting_line_lift import LiftingLineLift
from flight.lift.flat_plate_empirical_lift \
    import FlatPlateEmpiricalLift
from flight.drag.flat_plate_drag import FlatPlateDrag
from flight.drag.lifting_line_drag import LiftingLineDrag


class TestSurface(unittest.TestCase):

    def get_surface(self, relative_degrees):
        return Surface("test", Vector2D(0, 0), 0, Angle(relative_degrees),
                       10, None, None, Atmosphere())

    def test_lift_unit_leading_edge_positive_aoa(self):
        velocity = Vector2D(1, -1)
        surface = self.get_surface(0)
        lift_unit = Surface.get_lift_unit(surface.aoa(velocity), velocity)
        self.assertAlmostEqual(.7071, lift_unit.x, 4)
        self.assertAlmostEqual(.7071, lift_unit.y, 4)

    def test_lift_unit_leading_edge_negative_aoa(self):
        velocity = Vector2D(1, 1)
        surface = self.get_surface(0)
        lift_unit = Surface.get_lift_unit(surface.aoa(velocity), velocity)
        self.assertAlmostEqual(-.7071, lift_unit.x, 4)
        self.assertAlmostEqual(.7071, lift_unit.y, 4)

    def test_lift_unit_trailing_edge_positive_aoa(self):
        velocity = Vector2D(-1, -1)
        surface = self.get_surface(0)
        lift_unit = Surface.get_lift_unit(surface.aoa(velocity), velocity)
        self.assertAlmostEqual(-.7071, lift_unit.x, 4)
        self.assertAlmostEqual(.7071, lift_unit.y, 4)

    def test_lift_unit_trailing_edge_negative_aoa(self):
        velocity = Vector2D(-1, 1)
        surface = self.get_surface(0)
        lift_unit = Surface.get_lift_unit(surface.aoa(velocity), velocity)
        self.assertAlmostEqual(.7071, lift_unit.x, 4)
        self.assertAlmostEqual(.7071, lift_unit.y, 4)

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
    # http://www.aerospaceweb.org/question/flight/q0252.shtml

    # cessna from
    # http://www.aerospaceweb.org/question/flight/q0184.shtml

    def get_boeing_wing(self):
        wing_lift_curve = LinearLift(6.98, 0.29, 5.5)
        wing_drag_curve = LiftingLineDrag(6.98, 0.0305, 0.75)
        return Surface(
            "boeing wing", Vector2D(0, 0), 0, Angle(2.4), 510.97,
            wing_lift_curve, wing_drag_curve, Atmosphere())

    def get_cessna_wing(self):

        wing_lift_curve = LiftingLineLift(7.37)
        wing_drag_curve = LiftingLineDrag(7.37, 0.027, 0.75)
        return Surface(
            "cessna 172 wing", Vector2D(0, 0), 0, Angle(0), 16.2,
            wing_lift_curve, wing_drag_curve, Atmosphere())

    def get_lift(self, velocity, surface, angle):
        state = State(Vector2D(0, 0), velocity, angle, 0, Atmosphere())
        local_velocity = Simulator.get_local_airspeed(state)
        forces = surface.calculate_forces(local_velocity, 0, 12192)
        lift = [force for force in forces if force.name == "lift"]
        if len(lift) == 1:
            return lift[0].vector
        else:
            return None

    def get_lift_mag(self, velocity, surface, angle):
        vec = self.get_lift(velocity, surface, angle)
        if vec is not None:
            return vec.magnitude()
        else:
            return None

    def get_drag(self, velocity, surface, angle):

        forces = surface.calculate_forces(velocity.rotate(angle), 0, 12192)
        drag = [force for force in forces if force.name == "drag"]
        if len(drag) == 1:
            return drag[0].vector.magnitude()
        else:
            return None

    def test_boeing_lift(self):

        velocity = Vector2D(265.5, 0)
        surface = self.get_boeing_wing()
        lift = self.get_lift_mag(velocity, surface, Angle(0))

        self.assertAlmostEqual(2836530, lift, 0)

    def test_cessna_lift(self):

        velocity = Vector2D(100, 0)
        wing = self.get_cessna_wing()

        lift = self.get_lift_mag(velocity, wing, Angle(0))
        self.assertAlmostEqual(0, lift, 4, "0")

        lift = self.get_lift_mag(velocity, wing, Angle(1))
        self.assertAlmostEqual(2114.655024, lift, 4, "1")

        lift = self.get_lift_mag(velocity, wing, Angle(7))
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

    ############
    # FLAT PLATE
    ############

    def get_flat_plate(self):
        wing_lift_curve = FlatPlateEmpiricalLift(0)
        wing_drag_curve = FlatPlateDrag(0)
        return Surface("plate", Vector2D(0, 0), 0, Angle(0),
                       10, wing_lift_curve, wing_drag_curve,
                       Atmosphere())

    def test_flat_plate_lift(self):
        velocity = Vector2D(5, 0)
        wing = self.get_flat_plate()
        lift = self.get_lift(velocity, wing, Angle(10))
        self.assertAlmostEqual(6.5697617, lift.x, 4)
        self.assertAlmostEqual(37.2589703, lift.y, 4)

    def test_flat_plate_lift_neg(self):
        velocity = Vector2D(5, 0)
        wing = self.get_flat_plate()
        lift = self.get_lift(velocity, wing, Angle(-10))
        self.assertAlmostEqual(6.5697617, lift.x, 4)
        self.assertAlmostEqual(-37.2589703, lift.y, 4)

    def test_flat_plate_lift_neg_vert(self):
        velocity = Vector2D(5, 0)
        wing = self.get_flat_plate()
        lift = self.get_lift(velocity, wing, Angle(-90))
        self.assertAlmostEqual(0, lift.x, 4)
        self.assertAlmostEqual(0, lift.y, 4)

    def test_flat_plate_lift_neg_backward(self):
        velocity = Vector2D(5, 0)
        wing = self.get_flat_plate()
        lift = self.get_lift(velocity, wing, Angle(-170))
        self.assertAlmostEqual(-6.5697617, lift.x, 4)
        self.assertAlmostEqual(-37.2589703, lift.y, 4)

    def test_flat_plate_lift_pos_backward(self):
        velocity = Vector2D(5, 0)
        wing = self.get_flat_plate()
        lift = self.get_lift(velocity, wing, Angle(170))
        self.assertAlmostEqual(-6.5697617, lift.x, 4)
        self.assertAlmostEqual(37.2589703, lift.y, 4)


# Some code to make the tests actually run.
if __name__ == '__main__':
    unittest.main()
