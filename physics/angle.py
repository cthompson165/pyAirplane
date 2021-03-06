import math


class Angle:
    twoPi = math.pi * 2

    def __init__(self, degrees):
        self._degrees = Angle._normalize(degrees)
        self._radians = math.radians(self._degrees)

    def copy(self):
        return Angle(self._degrees)

    def type(self):
        return "angle"

    def degrees(self):
        return self._degrees

    def radians(self):
        return self._radians

    def plus(self, other):
        return Angle(self._degrees + other.degrees())

    def plus_constant(self, c):
        return Angle(self._degrees + c)

    def minus(self, other):
        return Angle(self._degrees - other.degrees())

    def minus_constant(self, c):
        return Angle(self._degrees - c)

    def times_constant(self, c):
        return Angle(self._degrees * c)

    def sin(self):
        return math.sin(self._radians)

    def cos(self):
        return math.cos(self._radians)

    def tan(self):
        return math.tan(self._radians)

    def relative_degrees(self):
        ''' 0 to 180 or 0 to -180 '''
        if (self._degrees >= 0 and self._degrees <= 180):
            return self._degrees
        else:
            return self._degrees - 360

    def relative_radians(self):
        ''' 0 to pi or 0 to -pi '''
        if (self._radians >= 0 and self._radians <= math.pi):
            return self._radians
        else:
            return self._radians - Angle.twoPi

    def _normalize(angle):
        while angle < 0:
            angle += 360
        while angle >= 360:
            angle -= 360
        return angle

    def __str__(self):
        return str(self._degrees)

    def __round__(self, places):
        return round(self._degrees, places)
