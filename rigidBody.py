import math
from vector2d import Vector2D
from force import Force
from state import State

class RigidBody:

    # Vector2D pos and vel. theta in degrees
    def __init__(self, mass, massMomentOfInertia, state):
        self.state = state
        self._mass = mass
        self._massMomentOfInertia = massMomentOfInertia

    def calculateForces(self, state):
        pass
        
    def calculateAcceleration(state, forces, mass, massMoment):   
        acceleration = Vector2D(0, 0)
        thetaAcceleration = 0
        for force in forces:
            forceAcceleration = force.vector.scale(1.0 / mass)
            acceleration = acceleration.add(forceAcceleration)

            forceTorque = force.pos.rotate(state.theta).cross(force.vector)
            thetaAcceleration += forceTorque / massMoment
     
        return [acceleration, thetaAcceleration]

    def calculateChange(self, state):
        forces = self.calculateForces(state)
        [acceleration, thetaAcceleration] = RigidBody.calculateAcceleration(state, forces, self._mass, self._massMomentOfInertia)
        return State(state.vel, acceleration, state.thetaVel, thetaAcceleration)

    def euler(self, t, state):
        stateDot = self.calculateChange(state)
        newState = state.add(stateDot.times(t))
        
        return newState

    def rungeKutta(self, t, state):
      
        f1 = self.calculateChange(state).times(t);
        f2 = self.calculateChange(state.add(f1.times(0.5))).times(t);
        f3 = self.calculateChange(state.add(f2.times(0.5))).times(t);
        f4 = self.calculateChange(state.add(f3)).times(t);
                
        newState = state.add(f1.add(f2.times(2)).add(f3.times(2)).add(f4).times(1.0/6))
        
        return newState

    def step(self, t):
        self.state = self.euler(t, self.state)
        
    def normalizeAngle(angle):
        while angle >= 360:
            angle -= 360
        while angle < 0:
            angle += 360
        return angle
