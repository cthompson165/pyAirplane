from physics.state import State


class Integrator:

    def integrate(self, state, time, change_calculation):
        raise NotImplementedError()

    def _add(self, state, state_change):
        new_pos = state.pos.add(state_change.vel)
        new_vel = state.vel.add(state_change.acc)
        new_theta = state.theta.plus_constant(state_change.theta_vel)
        new_theta_vel = state.theta_vel + state_change.theta_acc

        return State(new_pos, new_vel, new_theta, new_theta_vel)


class EulerIntegrator(Integrator):
    def integrate(self, state, time, change_calculation):
        state_dot = change_calculation(state)
        new_state = self._add(state, state_dot.multiply(time))

        return new_state


class RungeKuttaIntegrator(Integrator):

    def integrate(self, state, time, change_calculation):
        ''' integrate with runge kutta '''
        f_1 = change_calculation(state).multiply(time)
        f_2 = change_calculation(
            self.plus(state, (f_1.multiply(0.5)))).multiply(time)
        f_3 = change_calculation(
            self.plus(state, f_2.multiply(0.5))).multiply(time)
        f_4 = change_calculation(self.plus(state, f_3)).multiply(time)

        new_state = self._add(state, f_1.add(f_2.multiply(2)).add(
            f_3.multiply(2)).add(f_4).multiply(1.0/6))

        return new_state
