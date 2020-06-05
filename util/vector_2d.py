import math
from util.angle import Angle


class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def copy(self):
        return Vector2D(self.x, self.y)

    def cross(self, other):
        return self.x * other.y - self.y * other.x

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def add(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def subtract(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def scale(self, number):
        return Vector2D(self.x * number, self.y * number)

    def rotate(self, orientation):
        ''' rotates counter clockwise '''
        cos_val = orientation.cos()
        sin_val = orientation.sin()

        x_new = self.x * cos_val - self.y * sin_val
        y_new = self.x * sin_val + self.y * cos_val

        return Vector2D(x_new, y_new)

    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)

    def angle_with_other(self, other):
        angle = math.acos(
            self.dot(other) / (self.magnitude() * other.magnitude()))
        return Angle(math.degrees(angle))

    def angle(self):

        x = self.x
        y = self.y

        if x == 0 and y == 0:
            return Angle(0)  # TODO - error?
        elif x > 0 and y == 0:
            return Angle(0)
        elif x == 0 and y > 0:
            return Angle(90)
        elif x < 0 and y == 0:
            return Angle(180)
        elif x == 0 and y < 0:
            return Angle(270)

        angle_with_x = math.degrees(math.atan(self.y / self.x))

        if (x > 0 and y > 0):
            degrees = angle_with_x
        elif (x < 0 and y > 0):
            degrees = 180 + angle_with_x
        elif (x < 0 and y < 0):
            degrees = 180 + angle_with_x
        else:  # x > 0 and y < 0
            degrees = 360 + angle_with_x

        return Angle(degrees)

    def unit(self):
        if self.x == 0 and self.y == 0:
            return Vector2D(0, 0)
        else:
            mag = self.magnitude()
            return Vector2D(self.x / mag, self.y / mag)

    def reverse(self):
        return Vector2D(-self.x, -self.y)

    def array(self):
        return [self.x, self.y]

    def equals(self, other):
        return self.x == other.x and self.y == other.y

    def round(self, precision=None):
        return Vector2D(
            round(self.x, precision),
            round(self.y, precision))

    def __round__(self, precision):
        return self.round(precision)

    def __str__(self):
        return "[" + str(self.x) + ", " + str(self.y) + "]"

    def toint(self):
        return Vector2D(int(self.x), int(self.y))
