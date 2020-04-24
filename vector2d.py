import math


class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

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

    # theta in degrees - rotates counter clockwise
    def rotate(self, theta):
        theta = math.radians(theta)
        cos_val = math.cos(theta)
        sin_val = math.sin(theta)

        x_new = self.x * cos_val - self.y * sin_val
        y_new = self.x * sin_val + self.y * cos_val

        return Vector2D(x_new, y_new)

    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)

    def angle_with_other(self, other):
        angle = math.acos(
            self.dot(other) / (self.magnitude() * other.magnitude()))
        return math.degrees(angle)

    def angle(self):

        x = self.x
        y = self.y

        if x == 0 and y == 0:
            return 0  # TODO - error?
        elif x > 0 and y == 0:
            return 0
        elif x == 0 and y > 0:
            return 90
        elif x < 0 and y == 0:
            return 180
        elif x == 0 and y < 0:
            return 270

        angle_with_x = math.degrees(math.atan(self.y / self.x))

        if (x > 0 and y > 0):
            return angle_with_x
        elif (x < 0 and y > 0):
            return 180 + angle_with_x
        elif (x < 0 and y < 0):
            return 180 + angle_with_x
        else:  # x > 0 and y < 0
            return 360 + angle_with_x

    def unit(self):
        mag = self.magnitude()
        return Vector2D(self.x / mag, self.y / mag)

    def array(self):
        return [self.x, self.y]

    def equals(self, other):
        return self.x == other.x and self.y == other.y

    def round(self, precision):
        return Vector2D(
            round(self.x, precision),
            round(self.y, precision))

    def __str__(self):
        return "[" + str(self.x) + ", " + str(self.y) + "]"

    def toint(self):
        return Vector2D(int(self.x), int(self.y))