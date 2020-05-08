''' Rectangle rigid body '''
from physics.force import Force
from physics.rigid_body import RigidBody
from physics.state import State
from util.vector_2d import Vector2D


class Rectangle(RigidBody):
    ''' A rectangle that reacts realistically to forces applied at
    different locations
    WARNING - hasn't been tested since a lot of refactoring...'''

    def __init__(self, pos, theta, vel, angular_vel, length, width, cp):

        # a really big rectangle is too hard to rotate
        mass_length = length / 10
        mass_width = width / 10

        mass = mass_length * mass_width
        mass_moment_of_inertia = mass * (mass_length**2 + mass_width**2) / 12

        state = State(pos, vel, theta, angular_vel)
        RigidBody.__init__(self, mass, mass_moment_of_inertia, state)

        self._length = length
        self._width = width

        half_length = length / 2
        half_width = width / 2

        self._cp = cp
        self._forces = []

        self._vertices = [
            Vector2D(-half_length, -half_width),
            Vector2D(half_length, -half_width),
            Vector2D(half_length, half_width),
            Vector2D(-half_length, half_width)
        ]

    def calculate_forces(self, state):
        forces = self._forces
        self._forces = []
        return forces

    def _get_cp(self):
        return self._cp.rotate(self.state.theta).add(self.state.pos).array()

    def add_force_at_cp(self, force):
        ''' Add force at predefined "center of pressure" '''
        self._forces.append(Force("A force", self._cp, force))

    def get_vertices(self):
        ''' Get a list of points defining the rectangle '''
        new_points = []

        for point in self._vertices:
            new_point = point.rotate(self.state.theta).add(self.state.pos)
            new_points.append(new_point.array())

        return new_points
