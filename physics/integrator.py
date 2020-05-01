from physics.state import State

class Integrator:
    def integrate(self, changeCalculation):
        pass

    def add(self, state, stateChange):
        new_pos = state.pos.add(stateChange.vel)
        new_vel = state.vel.add(stateChange.acc)
        new_theta = state.theta.plusConstant(stateChange.theta_vel)
        new_theta_vel = state.theta_vel + stateChange.theta_acc

        return State(new_pos, new_vel, new_theta, new_theta_vel)

class EulerIntegrator(Integrator):
    def integrate(self, state, t, changeCalculation):
        state_dot = changeCalculation(state)
        new_state = self.add(state, state_dot.times(t))
        
        return new_state

class RungeKuttaIntegrator(Integrator):

    def integrate(self, state, t, changeCalculation):
      
        f1 = changeCalculation(state).times(t);
        f2 = changeCalculation(self.add(state, (f1.times(0.5)))).times(t)
        f3 = changeCalculation(self.add(state, f2.times(0.5))).times(t)
        f4 = changeCalculation(self.add(state, f3)).times(t)
                
        new_state = self.add(state, f1.add(f2.times(2)).add(f3.times(2)).add(f4).times(1.0/6))
        
        return new_state

