from util.angle import Angle
from util.vector_2d import Vector2D
from physics.state import State
from physics.force import Force
from physics.rigid_body import RigidBody
from game.kite.cell import Cell
import math


class BoxKite(RigidBody):
    def __init__(self, length, width, cell_length, bridle_length, knot_length):
        state = State(Vector2D(-10, 1), Vector2D(0, 0), Angle(80), 0)

        mass = 0.005  # TODO
        mass_moment_of_inertia = mass * (length**2 + width**2) / 12

        RigidBody.__init__(self, mass, mass_moment_of_inertia, state)

        bottom_front = Vector2D(length / 2.0, -width / 2.0)

        cos_bridle_angle = (knot_length**2 + length**2
                            - (bridle_length - knot_length)**2) \
            / (2 * knot_length * length)

        bridle_angle = math.acos(cos_bridle_angle)

        bridle_relative_x = -(length - knot_length * math.cos(bridle_angle))
        bridle_relative_y = -knot_length * math.sin(bridle_angle)
        bridle_position = bottom_front.add(
            Vector2D(bridle_relative_x, bridle_relative_y))

        front_surface_position = Vector2D(bottom_front.x, 0)
        back_surface_position = Vector2D(
            bottom_front.x - length + cell_length, 0)

        # adjust all positions so bridle position is at 0
        # to make torque calculations easier
        self.front_cell = Cell(
            "front", front_surface_position.subtract(bridle_position),
            cell_length, width)

        self.back_cell = Cell(
            "back", back_surface_position.subtract(bridle_position),
            cell_length, width)

        self._surfaces = []
        self._surfaces.append(self.front_cell)
        self._surfaces.append(self.back_cell)

        self.kite_cg = bridle_position.scale(-1)

    def calculate_local_forces(self, local_velocity, angular_velocity):
        local_forces = []
        for surface in self._surfaces:
            local_forces.extend(
                surface.calculate_forces(
                    local_velocity,
                    angular_velocity))
        return local_forces

    def calculate_global_forces(self, state):
        forces = []
        gravity = Force(Force.Source.gravity,
                        "gravity", self.kite_cg, self.weight())
        forces.append(gravity)
        return forces

    def convert_local_forces_to_global(self, state, local_forces):
        global_forces = []
        for local_force in local_forces:
            global_forces.append(local_force.rotate(state.theta))
        return global_forces

    def calculate_forces(self, state):

        wind_speed = Vector2D(3.2, 0)
        wind_state = State(
            state.pos, state.vel.add(wind_speed),
            state.theta, state.theta_vel)

        local_velocity = RigidBody.get_local_velocity(wind_state)
        angular_velocity = state.theta_vel

        local_forces = self.calculate_local_forces(
            local_velocity, angular_velocity)

        forces = self.convert_local_forces_to_global(state, local_forces)
        forces.extend(self.calculate_global_forces(state))

        force_sum = self.sum_forces(forces)

        string_force = self.calculate_string_force(state, force_sum)

        forces.append(Force(
             Force.Source.other, "String", Vector2D(0, 0), string_force))

        return forces

    def weight(self):
        return Vector2D(0, self.mass() * -9.8)

    def sum_forces(self, forces):
        sum = Vector2D(0, 0)
        for force in forces:
            sum = sum.add(force.vector)
        return sum

    def calculate_string_force(self, state, other_forces_sum):
        t1 = self.mass() * (state.pos.dot(state.vel))**2 \
            / state.pos.dot(state.pos)
        t2 = self.mass() * state.vel.dot(state.vel)
        t3 = state.pos.dot(other_forces_sum)

        scaling_constant = (t1 - t2 - t3) / state.pos.magnitude()
        N = state.pos.scale(1 / state.pos.magnitude())

        return N.scale(scaling_constant)
