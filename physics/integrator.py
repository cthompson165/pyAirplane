from physics.state import State

class Integrator:
    def integrate(self, changeCalculation):
        pass

    def add(self, state, stateChange):
        newPos = state.pos.add(stateChange.vel)
        newVel = state.vel.add(stateChange.acc)
        newTheta = state.theta.plusConstant(stateChange.thetaVel)
        newThetaVel = state.thetaVel + stateChange.thetaAcc

        return State(newPos, newVel, newTheta, newThetaVel)

class EulerIntegrator(Integrator):
    def integrate(self, state, t, changeCalculation):
        stateDot = changeCalculation(state)
        newState = self.add(state, stateDot.times(t))
        
        return newState

class RungeKuttaIntegrator(Integrator):

    def integrate(self, state, t, changeCalculation):
      
        f1 = changeCalculation(state).times(t);
        f2 = changeCalculation(self.add(state, (f1.times(0.5)))).times(t)
        f3 = changeCalculation(self.add(state, f2.times(0.5))).times(t)
        f4 = changeCalculation(self.add(state, f3)).times(t)
                
        newState = self.add(state, f1.add(f2.times(2)).add(f3.times(2)).add(f4).times(1.0/6))
        
        return newState

