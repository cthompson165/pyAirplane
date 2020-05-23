from physics.state import State


class Integrator:

    def integrate(self, rigid_body, time, change_calculation):
        raise NotImplementedError()

    @staticmethod
    def _add(state, state_change):
        new_pos = state.pos.add(state_change.vel)
        new_vel = state.vel.add(state_change.acc)
        new_theta = state.theta.plus_constant(state_change.theta_vel)
        new_theta_vel = state.theta_vel + state_change.theta_acc

        return State(new_pos, new_vel, new_theta, new_theta_vel)


class EulerIntegrator(Integrator):
    def integrate(self, rigid_body, time, change_calculation):
        state = rigid_body._state
        state_dot = change_calculation(rigid_body, state)
        new_state = self._add(state, state_dot.multiply(time))

        return new_state
