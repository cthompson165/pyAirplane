from util.vector_2d import Vector2D
from physics.rigid_body import RigidBody
from physics.integrator import EulerIntegrator


class Simulator:

    def __init__(self):
        self._rigid_bodies = []
        self._integrator = EulerIntegrator()

    def register(self, rigid_body):
        # TODO - make this a keyed collection and add deregister
        self._rigid_bodies.append(rigid_body)

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

    def _calculate_change(self, state, rigid_body):

        forces = rigid_body.calculate_forces(state)

        [acceleration, theta_acceleration] = \
            Simulator._calculate_acceleration(
                state, forces,
                self._mass, self._mass_moment_of_inertia)

        return self.StateChange(state.vel, acceleration,
                                state.theta_vel, theta_acceleration)

    def step(self, time):
        for rigid_body in self._rigid_bodies:
            ''' Apply forces and update state '''
            self._state = self._integrator.integrate(
                rigid_body._state, time, rigid_body._calculate_change)

    class StateChange:
        ''' Holds velocity and acceleration for use in integrators '''

        def __init__(self, vel, acc, theta_vel, theta_acc):
            self.vel = vel
            self.acc = acc
            self.theta_vel = theta_vel
            self.theta_acc = theta_acc

        def multiply(self, time):
            return RigidBody.StateChange(
                self.vel.scale(time), self.acc.scale(time),
                self.theta_vel * time, self.theta_acc * time)

        def add(self, other):
            return RigidBody.StateChange(
                self.vel.add(other.vel),
                self.acc.add(other.acc),
                self.theta_vel + other.theta_vel,
                self.theta_acc + other.theta_acc)
