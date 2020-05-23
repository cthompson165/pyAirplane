from util.vector_2d import Vector2D
from physics.integrator import EulerIntegrator
from physics.atmosphere import Atmosphere


class Simulator:

    def __init__(self):
        self._rigid_bodies = []
        self._integrator = EulerIntegrator()
        self.atmosphere = Atmosphere()

    def register(self, rigid_body):
        # TODO - make this a keyed collection and add deregister
        self._rigid_bodies.append(rigid_body)

    def step(self, time):
        for rigid_body in self._rigid_bodies:

            rigid_body._state.wind_speed = self.atmosphere.wind_speed

            ''' Apply forces and update state '''
            rigid_body._state = self._integrator.integrate(
                rigid_body, time, self._calculate_change)

    @staticmethod
    def _calculate_acceleration(state, forces, mass, mass_moment):
        acceleration = Vector2D(0, 0)
        theta_acceleration = 0
        for force in forces:
            force_acceleration = force.vector.scale(1.0 / mass)
            acceleration = acceleration.add(force_acceleration)
            force_torque = force.pos.cross(force.vector)
            theta_acceleration += force_torque / mass_moment

        return [acceleration, theta_acceleration]

    def _calculate_change(self, rigid_body, state):

        forces = rigid_body.calculate_forces(state, self.atmosphere)

        [acceleration, theta_acceleration] = \
            Simulator._calculate_acceleration(
                state, forces,
                rigid_body._mass, rigid_body._mass_moment_of_inertia)

        return Simulator.StateChange(state.vel, acceleration,
                                     state.theta_vel, theta_acceleration)

    class StateChange:
        ''' Holds velocity and acceleration for use in integrators '''

        def __init__(self, vel, acc, theta_vel, theta_acc):
            self.vel = vel
            self.acc = acc
            self.theta_vel = theta_vel
            self.theta_acc = theta_acc

        def multiply(self, time):
            return Simulator.StateChange(
                self.vel.scale(time), self.acc.scale(time),
                self.theta_vel * time, self.theta_acc * time)

        def add(self, other):
            return Simulator.StateChange(
                self.vel.add(other.vel),
                self.acc.add(other.acc),
                self.theta_vel + other.theta_vel,
                self.theta_acc + other.theta_acc)
