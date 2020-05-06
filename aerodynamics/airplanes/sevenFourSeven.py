import math
from util.vector2d import Vector2D
from aerodynamics.airplane import Airplane
from aerodynamics.surfaces.thinAirfoil import ThinAirfoil

class SevenFourSeven(Airplane):

    MAX_ELEVATOR_DEGREES = 10

    def __init__(self, pos, vel):
        Airplane.__init__(self, pos, vel)

        self._wing = ThinAirfoil("wing", Vector2D(0, 0), 2.4, 510.97, 6.98, 5.5, 0.29, 0.0305, 0.75)

        # TODO - figure out CLa
        self._horizontal_stabilizer = ThinAirfoil("stabilizer", Vector2D(-33, 0), 0, 136, 3.62, 0, 0, 0, 0.75)

        self._surfaces = []
        self._surfaces.append(self._wing)
        self._surfaces.append(self._horizontal_stabilizer)

    def apply_pitch_control(self, percent):
        self._horizontal_stabilizer.relative_degrees = SevenFourSeven.MAX_ELEVATOR_DEGREES * percent / 100.0

    def mass(self):
        return 289132.653061  # weight (F) / a (9.8)

    def massMomentOfInertia(self):
        length = 68.4
        height = 19.4
        radius = 4.5
        # cylinder
        # 1/12 * mass * length^2 + 1/4 * mass * radius^2
        return 1000000 #112875928
  
    def surfaces(self):
      return self._surfaces