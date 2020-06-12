import unittest
from util.vector_2d import Vector2D
from examples.projector import Projector


class TestProjector(unittest.TestCase):
    def test_projector_project(self):
        screen_size = Vector2D(10, 10)
        meters_per_pixel = 1
        projector = Projector(screen_size, meters_per_pixel)

        projected = projector.project(Vector2D(1, 1))

        self.assertEqual(1, projected.x)
        self.assertEqual(9, projected.y)

    def test_projector_project_scaled_down(self):
        screen_size = Vector2D(10, 10)
        meters_per_pixel = .5
        projector = Projector(screen_size, meters_per_pixel)

        projected = projector.project(Vector2D(1, 1))

        self.assertEqual(2, projected.x)
        self.assertEqual(8, projected.y)

    def test_projector_project_scaled_up(self):
        screen_size = Vector2D(10, 10)
        meters_per_pixel = 2
        projector = Projector(screen_size, meters_per_pixel)

        projected = projector.project(Vector2D(6, 6))

        self.assertEqual(3, projected.x)
        self.assertEqual(7, projected.y)

    def test_projector_center(self):
        screen_size = Vector2D(10, 10)
        meters_per_pixel = 1
        projector = Projector(screen_size, meters_per_pixel)

        projector.center(Vector2D(1, 1))
        projected = projector.project(Vector2D(1, 1))

        self.assertEqual(5, projected.x)
        self.assertEqual(5, projected.y)


if __name__ == '__main__':
    unittest.main()
