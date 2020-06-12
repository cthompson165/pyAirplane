from util.angle import Angle
from util.vector_2d import Vector2D
from physics.state import State
from physics.flying_object import FlyingObject
from physics.force import Force
from game.kite.cell import Cell


class BoxKite(FlyingObject):
    def __init__(self, length, width, cell_length,
                 atmosphere,
                 bridle=None,
                 initial_pos=None,
                 initial_orientation=Angle(70)):
        ''' Setup BoxKite. If a bridle is passed object in and the bridle
        has an initial position, the kite will calculate its initial position
        based on its current orientation and the bridle position. Otherwise
        it will used the passed in initial_pos '''

        mass = self.calculate_mass(length, width, cell_length, cell_length)
        mass_moment_of_inertia = mass * (length**2 + width**2) / 12
        bottom_back = Vector2D(-length / 2.0, -width / 2.0)

        if bridle is not None:
            self.bridle = bridle
            self.bridle_position = bottom_back.add(bridle.get_position())
            if bridle.initial_pos is not None:
                initial_pos = bridle.initial_pos.add(
                    self.bridle_position.reverse().rotate(initial_orientation))

        state = State(initial_pos,
                      Vector2D(0, 0), initial_orientation, 0,
                      atmosphere)

        FlyingObject.__init__(self, mass, mass_moment_of_inertia, state,
                              atmosphere)

        self.front_surface_position = Vector2D(bottom_back.x + length, 0)
        self.back_surface_position = Vector2D(bottom_back.x + cell_length, 0)

        self.front_cell = Cell(
            "front", self.front_surface_position,
            cell_length, width, atmosphere)

        self.back_cell = Cell(
            "back", self.back_surface_position,
            cell_length, width, atmosphere)

        self._surfaces = [self.front_cell, self.back_cell]

    def surfaces(self):
        return self._surfaces

    def global_bridle(self):
        return self.local_to_global(self.bridle_position)

    def total_lift(self):
        accumulator = Vector2D(0, 0)
        for force in self.local_forces():
            if force.source == Force.LIFT:
                accumulator = accumulator.add(force.vector)

        return accumulator

    def total_drag(self):
        accumulator = Vector2D(0, 0)
        for force in self.local_forces():
            if force.source == Force.DRAG:
                accumulator = accumulator.add(force.vector)

        return accumulator

    def calculate_mass(self, length, width, cell_length1, cell_length2):
        dowel_weight = .00216  # kg/m
        plastic_weight = .004752  # kg/m2

        area = (cell_length1 * width * 4 +
                cell_length2 * width * 4)

        cell_weight = area * plastic_weight
        stick_length = length * 4 + width * 4
        stick_weight = stick_length * dowel_weight

        return cell_weight + stick_weight
