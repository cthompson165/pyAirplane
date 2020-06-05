from util.angle import Angle
from util.vector_2d import Vector2D
from physics.state import State
from physics.flying_object import FlyingObject
from physics.point import Point
from game.kite.cell import Cell
from game.kite.bridle import Bridle
import math


class BoxKite(FlyingObject):
    def __init__(self, string_length, length, width, cell_length,
                 bridle_length, knot_length, initial_pos=None,
                 initial_orientation=Angle(70)):

        mass = self.calculate_mass(length, width, cell_length, cell_length)

        # get positions relative to cg

        self.back_back = Vector2D(-length / 2.0, 0)
        self.front = Vector2D(length / 2.0, 0)
        self.front_back = Vector2D(self.front.x - cell_length, 0)

        bottom_back = Vector2D(-length / 2.0, -width / 2.0)
        bridle = Bridle(bridle_length, knot_length, length)
        self.bridle_position = bottom_back.add(bridle.get_position())
        self.bridle_point = Point(self.bridle_position)
        self.front_surface_position = Vector2D(bottom_back.x + length, 0)
        self.back_surface_position = Vector2D(bottom_back.x + cell_length, 0)

        if initial_pos is None:
            initial_angle = math.asin(1/string_length)
            initial_x = math.cos(initial_angle) * string_length

            initial_bridle_global = Vector2D(-initial_x, 1)
            print("Initial: " +
                  str(round(initial_bridle_global.magnitude(), 2)))

            rotated_bridle_point = self.bridle_position.rotate(
                initial_orientation)

            initial_pos = initial_bridle_global.subtract(rotated_bridle_point)

            print("Bridle distance: " + str(round(initial_pos.add(
                self.bridle_position.rotate(
                    initial_orientation)).magnitude(), 3)))

        state = State(initial_pos,
                      Vector2D(0, 0), initial_orientation, 0)

        self.string_length = string_length

        mass_moment_of_inertia = mass * (length**2 + width**2) / 12

        FlyingObject.__init__(self, mass, mass_moment_of_inertia, state)

        self.front_cell = Cell(
            "front", self.front_surface_position,
            cell_length, width)

        self.back_cell = Cell(
            "back", self.back_surface_position,
            cell_length, width)

        self._surfaces = []
        self._surfaces.append(self.front_cell)
        self._surfaces.append(self.back_cell)

        # print(mass)
        # self.nasa(width * 100)

    def surfaces(self):
        return self._surfaces

    def nasa(self, w1):

        h1 = .5 * w1
        h2 = w1
        lbrid = 2.25 * w1
        lknot = 1.5 * w1

        wtarea = .0004752  # plastic
        wtlngs = .0216  # quarter birch dowel
        # wttail = .0004752  # 1" plastic

        # length: g/cm
        # area: g/cm2

        wtail = 0
        ltail = 0

        lkite = 2.0 * h1 + h2
        area = 4.0 * h1 * w1
        lengstk = 4.0 * lkite + 4.0 * w1
        weight = area * wtarea + lengstk * wtlngs + wtail
        cg = ((h1 + .5 * h2) * (weight - wtail) +
              wtail * (-ltail/2.0)) / weight
        cp = h1 + .5 * h2 + .25*h1
        ar = w1 / h1
        # kbase = w1 / 2.0

        print("NASA:")
        print("kite: " + str(w1) + "x" + str(lkite))
        print("Bridle: " + str(lbrid))
        print("Knot: " + str(lknot))
        print("Cell length: " + str(h1))

        print("cg: " + str(cg))
        print("cp: " + str(cp))
        print("ar: " + str(ar))
        print("weight: " + str(weight))

    def calculate_mass(self, length, width, cell_length1, cell_length2):
        dowel_weight = .00216  # kg/m
        plastic_weight = .004752  # kg/m2

        area = (cell_length1 * width * 4 +
                cell_length2 * width * 4)

        cell_weight = area * plastic_weight
        stick_length = length * 4 + width * 4
        stick_weight = stick_length * dowel_weight

        return cell_weight + stick_weight
