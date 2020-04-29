import math
from vector2d import Vector2D
from force import Force

class RigidBody:

    iterations = 0

    # Vector2D pos and vel. theta in degrees
    def __init__(self, mass, massMomentOfInertia, pos, theta, vel, angularVel):
        self._pos = pos  # CG
        self._vel = vel
        self._theta = theta
        self._angularVel = angularVel
        self._mass = mass
        self._massMomentOfInertia = massMomentOfInertia

    def pos(self):
        return self._pos

    def theta(self):
        return self._theta
  
    # TODO - can this be static and overridden?
    def calculateForces(self, pos, vel, theta, thetaVel):
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
        forces = self.calculateForces(state.pos, state.vel, state.theta, state.thetaVel)
        [acceleration, thetaAcceleration] = RigidBody.calculateAcceleration(state, forces, self._mass, self._massMomentOfInertia)
        return StateDot(state.vel, acceleration, state.thetaVel, thetaAcceleration)


    def euler(self, t):
        currentState = State(self._pos, self._vel, self._theta, self._angularVel)
        stateDot = self.calculateChange(currentState)
        newState = currentState.add(stateDot.times(t))

        self.updateState(newState)

        RigidBody.iterations += 1

    def rungeKutta(self, t):
        currentState = State(self._pos, self._vel, self._theta, self._angularVel)
      
        f1 = self.calculateChange(currentState).times(t);
        f2 = self.calculateChange(currentState.add(f1.times(0.5))).times(t);
        f3 = self.calculateChange(currentState.add(f2.times(0.5))).times(t);
        f4 = self.calculateChange(currentState.add(f3)).times(t);
                
        newState = currentState.add(f1.add(f2.times(2)).add(f3.times(2)).add(f4).times(1.0/6))
        self.updateState(newState)

        RigidBody.iterations += 1
        
    def updateState(self, newState):
        self._pos = newState.pos
        self._vel = newState.vel
        self._theta = newState.theta
        self._angularVel = newState.thetaVel

    def step(self, t):
        self.rungeKutta(t)
        #print ("pos: " + str(self._pos))
        #print ("vel: " + str(self._vel))
        
    def normalizeAngle(angle):
        while angle >= 360:
            angle -= 360
        while angle < 0:
            angle += 360
        return angle


class State:
    def __init__(self, pos, vel, theta, thetaVel):
        self.pos = pos
        self.vel = vel
        self.theta = theta
        self.thetaVel = thetaVel

    def add(self, stateDot):
        return State(
            self.pos.add(stateDot.vel),
            self.vel.add(stateDot.acc),
            self.theta + stateDot.thetaVel,
            self.thetaVel + stateDot.thetaAcc)
    
    def times(self, t):
        return State(
            self.pos.scale(t),
            self.vel.scale(t),
            self.theta * t,
            self.thetaVel * t)

class StateDot:
    def __init__(self, vel, acc, thetaVel, thetaAcc):
        self.vel = vel
        self.acc = acc
        self.thetaVel = thetaVel
        self.thetaAcc = thetaAcc
    
    def add(self, other):
        return StateDot(
            self.vel.add(other.vel),
            self.acc.add(other.acc),
            self.thetaVel + other.thetaVel,
            self.thetaAcc + other.thetaAcc)

    def times(self, t):
        return StateDot(
            self.vel.scale(t),
            self.acc.scale(t),
            self.thetaVel * t,
            self.thetaAcc * t)