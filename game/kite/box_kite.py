from util.angle import Angle
from util.vector_2d import Vector2D
from physics.state import State
from physics.force import Force
from physics.rigid_body import RigidBody
from physics.point import Point
from game.kite.cell import Cell
from game.kite.bridle import Bridle
import math


class BoxKite(RigidBody):
    def __init__(self, string_length, length, width, cell_length,
                 bridle_length, knot_length):

        mass = self.calculate_mass(length, width, cell_length, cell_length)
        initial_orientation = Angle(20)

        # get positions relative to cg
        bottom_back = Vector2D(-length / 2.0, -width / 2.0)
        bridle = Bridle(bridle_length, knot_length, length)
        self.bridle_position = bottom_back.add(bridle.get_position())
        self.bridle_point = Point(self.bridle_position)
        front_surface_position = Vector2D(bottom_back.x + length, 0)
        back_surface_position = Vector2D(bottom_back.x + cell_length, 0)

        initial_angle = math.asin(1/string_length)
        initial_x = math.cos(initial_angle) * string_length

        initial_bridle_global = Vector2D(-initial_x, 1)
        print("Initial: " + str(round(initial_bridle_global.magnitude(), 2)))

        rotated_bridle_point = self.bridle_position.rotate(initial_orientation)

        initial_pos = initial_bridle_global.subtract(rotated_bridle_point)

        print("Bridle distance: " + str(round(initial_pos.add(
            self.bridle_position.rotate(initial_orientation)).magnitude(), 3)))

        state = State(initial_pos,
                      Vector2D(0, 0), initial_orientation, 0)

        self.string_length = string_length

        mass_moment_of_inertia = mass * (length**2 + width**2) / 12

        RigidBody.__init__(self, mass, mass_moment_of_inertia, state)

        self.front_cell = Cell(
            "front", front_surface_position,
            cell_length, width)

        self.back_cell = Cell(
            "back", back_surface_position,
            cell_length, width)

        self._surfaces = []
        self._surfaces.append(self.front_cell)
        self._surfaces.append(self.back_cell)

        self.kite_cg = Vector2D(0, 0)

        self.on_string = True

    def calculate_local_forces(self, local_velocity, angular_velocity):
        local_forces = []
        for surface in self._surfaces:
            local_forces.extend(
                surface.calculate_forces(
                    local_velocity,
                    angular_velocity))
        return local_forces

    def calculate_mass(self, length, width, cell_length1, cell_length2):
        dowel_weight = .00216  # kg/m
        plastic_weight = .004752  # kg/m2

        cell_1_weight = cell_length1 * width * 4 * plastic_weight
        cell_2_weight = cell_length2 * width * 4 * plastic_weight
        stick_weight = dowel_weight * length * 4
        cross_piece_weight = dowel_weight * width * 4

        return cell_1_weight + cell_2_weight + \
            stick_weight + cross_piece_weight

    def calculate_global_forces(self, state):
        forces = []
        gravity = Force(Force.Source.gravity,
                        "gravity", self.kite_cg.rotate(state.theta),
                        self.weight())
        forces.append(gravity)
        return forces

    def convert_local_forces_to_global(self, state, local_forces):
        global_forces = []
        for local_force in local_forces:
            global_forces.append(local_force.rotate(state.theta))
        return global_forces

    def cut_string(self):
        self.on_string = False

    def calculate_forces(self, state, atmosphere):

        local_velocity = RigidBody.get_local_airspeed(state)
        angular_velocity = state.theta_vel

        local_forces = self.calculate_local_forces(
            local_velocity, angular_velocity)

        forces = self.convert_local_forces_to_global(state, local_forces)
        forces.extend(self.calculate_global_forces(state))

        '''
        if self.on_string:
            force_sum = self.sum_forces(forces)
            string_force = self.calculate_string_force(state, force_sum)
            forces.append(Force(
                Force.Source.other, "String",
                self.bridle_point.position, string_force))
        '''
        # print("Orientation: " + str(round(state.theta, 2)))
        print("Height: " + str(round(state.pos.y, 2)))
        print("Bridle distance: " + str(round(state.pos.add(
            self.bridle_position.rotate(state.theta)).magnitude(), 3)))
        # print("Airspeed: " + str(round(state.airspeed(), 2)))

        '''
        print("FORCES:")
        for force in forces:
            print("\t" + force.name + " " +
                  str(round(force.vector, 2)))
        '''
        print("------")

        return forces

    def weight(self):
        return Vector2D(0, self.mass() * -9.8)

    def sum_forces(self, forces):
        sum = Vector2D(0, 0)
        for force in forces:
            sum = sum.add(force.vector)
        return sum

    def calculate_string_force(self, state, other_forces_sum):

        # need to find velocity relative to the string which is ground-based
        # so use global coordinates and ground speed
        bridle_position = state.pos
        bridle_velocity = state.ground_speed()

        alpha = 1
        beta = 1

        distance = bridle_position.magnitude()
        if distance < (self.string_length - 1):
            # TODO - how small a number under string length
            # we can get away with. 1 is too big
            return Vector2D(0, 0)  # don't apply force
        elif distance > (self.string_length + 3):
            self.cut_string()
            return Vector2D(0, 0)
        else:
            N = bridle_position.scale(1/distance)

            print("distance: " + str(round(distance)))

            N_dot_term = bridle_position.dot(bridle_velocity) \
                / bridle_position.dot(bridle_position)
            N_dot = bridle_velocity.subtract(bridle_position.scale(N_dot_term))
            N_dot = N_dot.scale(1 / distance)

            N_dot_N = N.dot(N)

            C = distance - self.string_length
            C_dot = N.dot(bridle_velocity)

            t1 = self.mass() * N_dot.dot(bridle_velocity)
            t2 = N.dot(other_forces_sum)
            feedback_term = self.mass() * (alpha * C + beta * C_dot)

            scaling_constant = (-t1 - t2 - feedback_term) / N_dot_N

            return N.scale(scaling_constant)
