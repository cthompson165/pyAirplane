from util.vector2d import Vector2D
from physics.integrator import EulerIntegrator

class RigidBody:

    # Vector2D pos and vel. theta in degrees
    def __init__(self, mass, massMomentOfInertia, state):
        self.state = state
        self._mass = mass
        self._massMomentOfInertia = massMomentOfInertia

        self._integrator = EulerIntegrator()

    def calculateForces(self, state):
        pass
        
    def calculateAcceleration(state, forces, mass, massMoment):   
        acceleration = Vector2D(0, 0)
        thetaAcceleration = 0
        for force in forces:
            forceAcceleration = force.vector.scale(1.0 / mass)
            acceleration = acceleration.add(forceAcceleration)

            forceTorque = force.pos.rotate(state.theta).cross(force.vector)

            # TODO - figure out the right damping constant 
            # to prevent all the oscillating...
            forceTorque -= 10000 * state.thetaVel

            thetaAcceleration += forceTorque / massMoment
     
        return [acceleration, thetaAcceleration]

    def calculateChange(self, state):
        forces = self.calculateForces(state)
        [acceleration, thetaAcceleration] = RigidBody.calculateAcceleration(state, forces, self._mass, self._massMomentOfInertia)
        return StateChange(state.vel, acceleration, state.thetaVel, thetaAcceleration)

    def step(self, t):
        self.state = self._integrator.integrate(self.state, t, self.calculateChange)

class StateChange:
    def __init__(self, vel, acc, thetaVel, thetaAcc):
        self.vel = vel
        self.acc = acc
        self.thetaVel = thetaVel
        self.thetaAcc = thetaAcc
    
    def times(self, t):
        return StateChange(self.vel.scale(t), self.acc.scale(t), self.thetaVel * t, self.thetaAcc * t)

    def add(self, other):
        return StateChange(self.vel.add(other.vel), self.acc.add(other), self.thetaVel + other.thetaVel, self.thetaAcc + other.thetaAcc)

