import math
from rigidBody import RigidBody
from vector import Vector2D

class Rectangle(RigidBody):
    
    def __init__(this, pos, theta, vel, angularVel, length, width, cp):

      # a really big rectangle is too hard to rotate
      massLength = length / 10
      massWidth = width / 10

      mass = massLength * massWidth
      massMomentOfInertia = mass * (massLength**2 + massWidth**2) / 12

      RigidBody.__init__(this, mass, massMomentOfInertia, pos, theta, vel, angularVel)

      this._length = length
      this._width = width

      half_length = length / 2
      half_width = width / 2

      this._cp = cp
      
      this._vertices = [
        Vector2D([-half_length, -half_width]),
        Vector2D([half_length, -half_width]),
        Vector2D([half_length, half_width]),
        Vector2D([-half_length, half_width])
      ]

    def get_cp(this):
      return this._cp.rotate(this._theta).add(this._pos).array()

    def addForceAtCp(this, force):
      this.addForce(this._cp, force)

    def get_vertices(this):
    
      new_points = []

      for point in this._vertices:
          new_point = point.rotate(this._theta).add(this._pos)
          new_points.append(new_point.array())
    
      return new_points