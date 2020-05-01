import unittest
from util.vector2d import Vector2D
from aerodynamics.surface import Surface
from util.angle import Angle


class TestSurface(unittest.TestCase):

    def getSurface(self, relativeDegrees):
        return Surface("test", Vector2D(0, 0), relativeDegrees, 0)

    def testSurfaceAoA(self):
        surface = self.getSurface(0)
        aoa = surface.AoA(Angle(0), Vector2D(100, 0))
        self.assertAlmostEqual(0, aoa.relativeDegrees())
    
    def testSurfaceAoAPositive(self):
        surface = self.getSurface(0)
        aoa = surface.AoA(Angle(5), Vector2D(100, 0))
        self.assertAlmostEqual(5, aoa.relativeDegrees())

    def testSurfaceAoANegative(self):
        surface = self.getSurface(0)
        aoa = surface.AoA(Angle(-5), Vector2D(100, 0))
        self.assertAlmostEqual(-5, aoa.relativeDegrees())

    def testSurfaceAoARotated(self):
        surface = self.getSurface(0)
        aoa = surface.AoA(Angle(47), Vector2D(100, 100))
        self.assertAlmostEqual(2, aoa.relativeDegrees())

    def testSurfaceAoARotatedHugePos(self):
        surface = self.getSurface(0)
        aoa = surface.AoA(Angle(223), Vector2D(100, 100))
        self.assertAlmostEqual(178, aoa.relativeDegrees())

    def testSurfaceAoARotatedHugeNeg(self):
        surface = self.getSurface(0)
        aoa = surface.AoA(Angle(227), Vector2D(100, 100))
        self.assertAlmostEqual(-178, aoa.relativeDegrees())

    def testSurfaceAoAWithRelative(self):
        surface = self.getSurface(3)
        aoa = surface.AoA(Angle(42), Vector2D(100, 100))
        self.assertAlmostEqual(0, aoa.relativeDegrees())

    def testSurfaceAoAWithRelativePositive(self):
        surface = self.getSurface(3)
        aoa = surface.AoA(Angle(45), Vector2D(100, 100))
        self.assertAlmostEqual(3, aoa.relativeDegrees())
    
    def testSurfaceAoAWithRelativeNegative(self):
        surface = self.getSurface(3)
        aoa = surface.AoA(Angle(40), Vector2D(100, 100))
        self.assertAlmostEqual(-2, aoa.relativeDegrees())

# Some code to make the tests actually run.
if __name__ == '__main__':
    unittest.main()
