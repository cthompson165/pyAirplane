import unittest
from util.vector_2d import Vector2D
from util.projector import Projector


class TestProjector(unittest.TestCase):
    def testProjectorProject(self):
        screenSize = Vector2D(10, 10)
        metersPerPixel = 1
        projector = Projector(screenSize, metersPerPixel)

        projected = projector.project(Vector2D(1, 1))

        self.assertEqual(1, projected.x)
        self.assertEqual(9, projected.y)

    def testProjectorProjectScaledDown(self):
        screenSize = Vector2D(10, 10)
        metersPerPixel = .5
        projector = Projector(screenSize, metersPerPixel)

        projected = projector.project(Vector2D(1, 1))

        self.assertEqual(2, projected.x)
        self.assertEqual(8, projected.y)

    def testProjectorProjectScaledUp(self):
        screenSize = Vector2D(10, 10)
        metersPerPixel = 2
        projector = Projector(screenSize, metersPerPixel)

        projected = projector.project(Vector2D(6, 6))

        self.assertEqual(3, projected.x)
        self.assertEqual(7, projected.y)

    def testProjectorCenter(self):
        screenSize = Vector2D(10, 10)
        metersPerPixel = 1
        projector = Projector(screenSize, metersPerPixel)

        projector.center(Vector2D(1, 1))
        projected = projector.project(Vector2D(1, 1))

        self.assertEqual(5, projected.x)
        self.assertEqual(5, projected.y)


if __name__ == '__main__':
    unittest.main()
