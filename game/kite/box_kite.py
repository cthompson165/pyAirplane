from util.angle import Angle
from util.vector_2d import Vector2D
from physics.state import State
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

        self.on_string = True

    def surfaces(self):
        return self._surfaces

    def calculate_mass(self, length, width, cell_length1, cell_length2):
        dowel_weight = .00216  # kg/m
        plastic_weight = .004752  # kg/m2

        cell_1_weight = cell_length1 * width * 4 * plastic_weight
        cell_2_weight = cell_length2 * width * 4 * plastic_weight
        stick_weight = dowel_weight * length * 4
        cross_piece_weight = dowel_weight * width * 4

        return cell_1_weight + cell_2_weight + \
            stick_weight + cross_piece_weight

    def cut_string(self):
        self.on_string = False
