from util.angle import Angle
from util.vector_2d import Vector2D
from physics.state import State
from physics.flying_object import FlyingObject
from game.kite.cell import Cell


class SurfacelessKite(FlyingObject):
    def __init__(self, length, width, atmosphere,
                 initial_pos,
                 initial_orientation=Angle(0)):

        mass = 2
        state = State(initial_pos,
                      Vector2D(0, 0), initial_orientation, 0,
                      atmosphere)
        mass_moment_of_inertia = mass * (length**2 + width**2) / 12
        FlyingObject.__init__(self, mass, mass_moment_of_inertia, state,
                              atmosphere)

        cell_length = length / 3.0

        cell_position = length / 2
        front_cell = Cell("front", Vector2D(cell_position, 0),
                          cell_length, width, atmosphere)

        cell_position = -(length / 2) + cell_length
        back_cell = Cell("back", Vector2D(cell_position, 0),
                         cell_length, width, atmosphere)

        self._surfaces = [front_cell, back_cell]

    def surfaces(self):
        return self._surfaces
