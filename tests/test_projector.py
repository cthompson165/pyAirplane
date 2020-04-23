import unittest
from vector import Vector2D
from projector import Projector


class TestProjector(unittest.TestCase):
    def test_projector_project(self):
        screen_size = Vector2D([10, 10])
        meters_per_pixel = 1
        projector = Projector(screen_size, meters_per_pixel)

        projected = projector.project(Vector2D([1, 1]))

        self.assertEquals(1, projected.x())
        self.assertEquals(9, projected.y())
    
    def test_projector_project_scaled_down(self):
        screen_size = Vector2D([10, 10])
        meters_per_pixel = .5
        projector = Projector(screen_size, meters_per_pixel)

        projected = projector.project(Vector2D([1, 1]))

        self.assertEquals(2, projected.x())
        self.assertEquals(8, projected.y())

    def test_projector_project_scaled_up(self):
        screen_size = Vector2D([10, 10])
        meters_per_pixel = 2
        projector = Projector(screen_size, meters_per_pixel)

        projected = projector.project(Vector2D([6, 6]))

        self.assertEquals(3, projected.x())
        self.assertEquals(7, projected.y())

    def test_projector_center(self):
        screen_size = Vector2D([10, 10])
        meters_per_pixel = 1
        projector = Projector(screen_size, meters_per_pixel)

        projector.center(Vector2D([1, 1]))
        projected = projector.project(Vector2D([1, 1]))

        self.assertEquals(5, projected.x())
        self.assertEquals(5, projected.y())

    #TODO - test another object that isn't centered

# Some code to make the tests actually run.
if __name__ == '__main__':
    unittest.main()