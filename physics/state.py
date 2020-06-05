from util.vector_2d import Vector2D


class State:
    def __init__(self, pos, vel, theta, theta_vel):

        self.pos = pos  # vector
        self.vel = vel  # vector
        self.theta = theta  # angle
        self.theta_vel = theta_vel  # int

        self.wind_speed = Vector2D(0, 0)

    def ground_speed(self):
        return self.vel

    def airspeed(self):
        return self.vel.subtract(self.wind_speed)

    def copy(self):
        return State(self.pos.copy(), self.vel.copy(), self.theta.copy(),
                     self.theta_vel)

    def __str__(self):
        return ("pos: " + str(self.pos.round(4)) +
                "\nvel: " + str(self.vel.round(4)) +
                "\nvel mag: " + str(round(self.vel.magnitude())) +
                "\nvel angle: " + str(round(self.vel.angle(), 4)) +
                "\norientation: " + str(round(self.theta, 4)) +
                "\nangular vel: " + str(round(self.theta_vel, 4)))
