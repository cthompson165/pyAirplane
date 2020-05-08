from util.vector_2d import Vector2D
from physics.integrator import EulerIntegrator

class RigidBody:

    # Vector2D pos and vel. theta in degrees
    def __init__(self, mass, mass_moment_of_inertia, state):
        self.state = state
        self._mass = mass
        self._mass_moment_of_inertia = mass_moment_of_inertia

        self._integrator = EulerIntegrator()

    def calculate_forces(self, state):
        pass
        
    def calculate_acceleration(state, forces, mass, mass_moment):   
        acceleration = Vector2D(0, 0)
        theta_acceleration = 0
        for force in forces:
            force_acceleration = force.vector.scale(1.0 / mass)
            acceleration = acceleration.add(force_acceleration)

            force_torque = force.pos.rotate(state.theta).cross(force.vector)

            theta_acceleration += force_torque / mass_moment
     
        return [acceleration, theta_acceleration]

    def calculate_change(self, state):
        forces = self.calculate_forces(state)
        [acceleration, theta_acceleration] = RigidBody.calculate_acceleration(state, forces, self._mass, self._mass_moment_of_inertia)
        return StateChange(state.vel, acceleration, state.theta_vel, theta_acceleration)

    def step(self, t):
        self.state = self._integrator.integrate(self.state, t, self.calculate_change)

class StateChange:
    def __init__(self, vel, acc, theta_vel, theta_acc):
        self.vel = vel
        self.acc = acc
        self.theta_vel = theta_vel
        self.theta_acc = theta_acc
    
    def times(self, t):
        return StateChange(self.vel.scale(t), self.acc.scale(t), self.theta_vel * t, self.theta_acc * t)

    def plus(self, other):
        return StateChange(self.vel.add(other.vel), self.acc.add(other), self.theta_vel + other.theta_vel, self.theta_acc + other.theta_acc)

