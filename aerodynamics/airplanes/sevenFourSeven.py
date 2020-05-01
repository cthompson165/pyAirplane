import math
from util.vector2d import Vector2D
from aerodynamics.airplane import Airplane
from aerodynamics.surfaces.thinAirfoil import ThinAirfoil

class SevenFourSeven(Airplane):
    def __init__(self, pos, vel):
        Airplane.__init__(self, pos, vel)

        self._surfaces = []
        self._surfaces.append(ThinAirfoil("wing", Vector2D(0, 0), 2.4, 510.97, 5.5, 0.29))

        # TODO - figure out CLa
        self._surfaces.append(ThinAirfoil("stabilizer", Vector2D(-33, 0), 0, 136, 2 * math.pi, 0))

    def setElevatorTo(self, degrees):
        self._surfaces[1].relativeDegrees = degrees
        pass

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