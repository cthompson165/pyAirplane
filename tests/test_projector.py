import unittest
from physics.vector_2d import Vector2D
import display


class TestProjector(unittest.TestCase):
    def test_projector_project(self):
        screen_size = Vector2D(10, 10)
        meters_per_pixel = 1
        projector = display.Projector(screen_size, meters_per_pixel)

        projected = projector.project(Vector2D(1, 1))

        self.assertEqual(1, projected[0])
        self.assertEqual(9, projected[1])

    def test_projector_project_scaled_down(self):
        screen_size = Vector2D(10, 10)
        meters_per_pixel = .5
        projector = display.Projector(screen_size, meters_per_pixel)

        projected = projector.project(Vector2D(1, 1))

        self.assertEqual(2, projected[0])
        self.assertEqual(8, projected[1])

    def test_projector_project_scaled_up(self):
        screen_size = Vector2D(10, 10)
        meters_per_pixel = 2
        projector = display.Projector(screen_size, meters_per_pixel)

        projected = projector.project(Vector2D(6, 6))

        self.assertEqual(3, projected[0])
        self.assertEqual(7, projected[1])

    def test_projector_center(self):
        screen_size = Vector2D(10, 10)
        meters_per_pixel = 1
        projector = display.Projector(screen_size, meters_per_pixel)

        projector.center(Vector2D(1, 1))
        projected = projector.project(Vector2D(1, 1))

        self.assertEqual(5, projected[0])
        self.assertEqual(5, projected[1])


if __name__ == '__main__':
    unittest.main()
