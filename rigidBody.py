import math
from vector2d import Vector2D


class RigidBody:

    # Vector2D pos and vel. theta in degrees
    def __init__(this, mass, massMomentOfInertia, pos, theta, vel, angularVel):
        this._pos = pos  # CG
        this._vel = vel
        this._theta = theta
        this._angularVel = angularVel
        this._mass = mass
        this._massMomentOfInertia = massMomentOfInertia
        this.resetForces()

    def pos(self):
        return self._pos

    def theta(this):
        return this._theta

    def resetForces(this):
        this._force = Vector2D(0, 0)
        this._torque = 0

    # Vector2D force, point. point is in initial frame
    def addForce(this, point, force):
        this._force = this._force.add(force)
        this._torque += point.rotate(this._theta).cross(force)
        
    def __applyForces(this, t):

        acceleration = this._force.scale(1 / this._mass)
        this._vel = this._vel.add(acceleration.scale(t))
        this._angularVel += this._torque / this._massMomentOfInertia

    def move(this, t):
        this.__applyForces(t)
        this._pos = this._pos.add(this._vel)
        this._theta = (this._theta + this._angularVel) % 360
