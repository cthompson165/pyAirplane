from util.vector_2d import Vector2D


class State:
    def __init__(self, position, velocity, orientation, angular_velocity):

        self.position = position  # vector
        self.velocity = velocity  # vector
        self.orientation = orientation  # angle
        self.angular_velocity = angular_velocity  # int

        self.wind_speed = Vector2D(0, 0)

    def ground_speed(self):
        return self.velocity

    def airspeed(self):
        return self.velocity.subtract(self.wind_speed)

    def copy(self):
        return State(
            self.position.copy(), self.velocity.copy(),
            self.orientation.copy(),
            self.angular_velocity)

    def __str__(self):
        return ("position: " + str(self.position.round(4)) +
                "\nvel: " + str(self.velocity.round(4)) +
                "\nvel mag: " + str(round(self.velocity.magnitude())) +
                "\nvel angle: " + str(round(self.velocity.angle(), 4)) +
                "\norientation: " + str(round(self.orientation, 4)) +
                "\nangular velocity: " + str(round(self.angular_velocity, 4)))
