from vector2d import Vector2D
from airplane import Airplane
from airfoil import Airfoil

class SevenFourSeven(Airplane):
    def __init__(self, pos, vel):
        Airplane.__init__(self, pos, vel)

        self._airfoils = []
        self._airfoils.append(Airfoil(Vector2D(-3, 0), 0, 510.97, 5.5, 0.29))

    def mass(self):
        return 289132.653061  # weight (F) / a (9.8)

    def massMomentOfInertia(self):
        length = 68.4
        height = 19.4
        return self.mass() * (length**2 + height**2) / 12  # rectangle...

    def airfoils(self):
      return self._airfoils