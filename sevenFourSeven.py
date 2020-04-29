import math
from vector2d import Vector2D
from airplane import Airplane
from airfoil import Airfoil

class SevenFourSeven(Airplane):
    def __init__(self, pos, vel):
        Airplane.__init__(self, pos, vel)

        self._airfoils = []
        self._airfoils.append(Airfoil("wing", Vector2D(0, 0), 2.4, 510.97, 5.5, 0.29))

        # TODO - figure out CLa
        self._airfoils.append(Airfoil("stabilizer", Vector2D(-33, 0), 0, 136, 2 * math.pi, 0))

    def changeElevator(self, angle):
        #self._airfoils[1].debugPrint = True
        self._airfoils[1].relativeAoA = angle

    def mass(self):
        return 289132.653061  # weight (F) / a (9.8)

    def massMomentOfInertia(self):
        length = 68.4
        height = 19.4
        radius = 4.5
        # cylinder
        # 1/12 * mass * length^2 + 1/4 * mass * radius^2
        return 1000000 #112875928
        

    def airfoils(self):
      return self._airfoils