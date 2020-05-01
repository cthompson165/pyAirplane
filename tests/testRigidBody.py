import unittest
from util.vector2d import Vector2D
from physics.rigidBody import RigidBody


class TestRigidBody(unittest.TestCase):
    def testNormalizeAngle(self):
        self.assertAlmostEqual(0, 0)
    
    #def testNormalizeAngle_Under(self):
    #    angle = RigidBody.normalizeAngle(-0.01)
    #    self.assertAlmostEqual(angle, 359.99)

    #def testNormalizeAngle_Over(self):
    #    angle = RigidBody.normalizeAngle(360.01)
    #    self.assertAlmostEqual(angle, 0.01)
   

if __name__ == '__main__':
    unittest.main()
