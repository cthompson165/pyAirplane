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

    def add(self, other):
        return State(
            self.pos.add(other.pos), self.vel.add(other.vel),
            self.theta.plus(other.theta), self.theta_vel + other.theta_vel)

    def times(self, t):
        return State(
            self.pos.scale(t), self.vel.scale(t), self.theta.times_constant(t),
            self.theta_vel * t)

    def __str__(self):
        return ("pos: " + str(self.pos.round(4)) +
                "\nvel: " + str(self.vel.round(4)) +
                "\nvel mag: " + str(round(self.vel.magnitude())) +
                "\nvel angle: " + str(round(self.vel.angle(), 4)) +
                "\norientation: " + str(round(self.theta, 4)) +
                "\nangular vel: " + str(round(self.theta_vel, 4)))
