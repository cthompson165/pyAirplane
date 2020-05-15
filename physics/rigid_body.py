from util.vector_2d import Vector2D
from physics.integrator import EulerIntegrator


class RigidBody:
    ''' Calculates state based on forces '''

    # Vector2D pos and vel. theta in degrees
    def __init__(self, mass, mass_moment_of_inertia, state):
        self.state = state
        self._mass = mass
        self._mass_moment_of_inertia = mass_moment_of_inertia

        self._integrator = EulerIntegrator()

    def mass(self):
        return self._mass

    def calculate_local_forces(self, state):
        ''' Get all the forces applied to the object '''
        raise NotImplementedError()

    def calculate_global_forces(self, state):
        raise NotImplementedError()

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

    def _convert_to_global(self, local_forces):
        global_forces = []
        for local_force in local_forces:
            global_forces.append(local_force.rotate(self.state.theta))
        return global_forces

    def _calculate_change(self, state):

        local_velocity = state.vel.rotate(state.theta.times_constant(-1))
        local_forces = self.calculate_local_forces(
            local_velocity, state.theta_vel)

        global_forces = self._convert_to_global(local_forces)
        global_forces.extend(self.calculate_global_forces(state))

        [acceleration, theta_acceleration] = \
            RigidBody._calculate_acceleration(
                state, global_forces,
                self._mass, self._mass_moment_of_inertia)

        return self.StateChange(state.vel, acceleration,
                                state.theta_vel, theta_acceleration)

    def step(self, time):
        ''' Apply forces and update state '''
        self.state = self._integrator.integrate(
            self.state, time, self._calculate_change)

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
                self.vel.add(other.vel), self.acc.add(other),
                self.theta_vel + other.theta_vel,
                self.theta_acc + other.theta_acc)
