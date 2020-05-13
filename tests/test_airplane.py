import unittest
from util.vector_2d import Vector2D
from physics.state import State
from aerodynamics.surface import Surface


class TestAirplane(unittest.TestCase):

    def test_calculate_velocity_from_rotation_rear_surface(self):

        # airplane rotating back
        state = State(Vector2D(0, 0), Vector2D(0, 0), 0, 3)

        # surface is behind the cg on y axis
        surface = Surface("test", Vector2D(-10, 0), 0, 0, None, None)
        vel_rot = surface.calculate_velocity_from_rotation(state)

        self.assertAlmostEqual(-0.524, vel_rot.y, 3)
        self.assertAlmostEqual(0, vel_rot.x)

    def test_calculate_velocity_from_rotation_forward_surface(self):

        # airplane rotating back
        state = State(Vector2D(0, 0), Vector2D(0, 0), 0, 3)

        # surface is in front of cg on y axis
        surface = Surface("test", Vector2D(10, 0), 0, 0, None, None)
        vel_rot = surface.calculate_velocity_from_rotation(state)

        self.assertAlmostEqual(0.524, vel_rot.y, 3)
        self.assertAlmostEqual(0, vel_rot.x)


# Some code to make the tests actually run.
if __name__ == '__main__':
    unittest.main()
