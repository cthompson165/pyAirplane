import math


class Vector2D:
    def __init__(this, array):
        this._v = array

    def x(this):
        return this._v[0]

    def y(this):
        return this._v[1]

    def cross(this, other):
        return this.x() * other.y() - this.y() * other.x()

    def dot(this, other):
        return this.x() * other.x() + this.y() * other.y()

    def add(this, other):
        return Vector2D([this.x() + other.x(), this.y() + other.y()])

    def subtract(this, other):
        return Vector2D([this.x() - other.x(), this.y() - other.y()])

    def scale(this, number):
        return Vector2D([this.x() * number, this.y() * number])

    # theta in degrees - rotates counter clockwise
    def rotate(this, theta):
        theta = math.radians(theta)
        cos_val = math.cos(theta)
        sin_val = math.sin(theta)

        x_new = this.x() * cos_val - this.y() * sin_val
        y_new = this.x() * sin_val + this.y() * cos_val

        return Vector2D([x_new, y_new])

    def magnitude(this):
        return math.sqrt(this.x()**2 + this.y()**2)

    def angle_with_other(this, other):
        angle = math.acos(
            this.dot(other) / (this.magnitude() * other.magnitude()))
        return math.degrees(angle)

    def angle(this):
        # TODO - better way to do this?
        x = this.x()
        y = this.y()

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

        angle_with_x = math.degrees(math.atan(this.y() / this.x()))

        if (x > 0 and y > 0):
            return angle_with_x
        elif (x < 0 and y > 0):
            return 180 + angle_with_x
        elif (x < 0 and y < 0):
            return 180 + angle_with_x
        else:  # x > 0 and y < 0
            return 360 + angle_with_x

    def unit(this):
        mag = this.magnitude()
        return Vector2D([this.x() / mag, this.y() / mag])

    def array(this):
        return [this.x(), this.y()]

    def equals(this, other):
        return this.x() == other.x() and this.y() == other.y()

    def round(this, precision):
        return Vector2D(
            [round(this._v[0], precision),
             round(this._v[1], precision)])

    def __str__(this):
        return str(this._v)

    def toint(this):
        return Vector2D([int(this._v[0]), int(this._v[1])])