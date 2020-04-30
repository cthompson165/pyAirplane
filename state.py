class State:
    def __init__(self, pos, vel, theta, thetaVel):
        self.pos = pos
        self.vel = vel
        self.theta = theta
        self.thetaVel = thetaVel

    def add(self, other):
        return State(
            self.pos.add(other.pos), self.vel.add(other.vel),
            self.theta + other.theta, self.thetaVel + other.thetaVel)

    def times(self, t):
        return State(
            self.pos.scale(t), self.vel.scale(t), self.theta * t,
            self.thetaVel * t)

    def __str__(self):
        return "pos: " + str(self.pos) + "\nvel: " + str(
            self.vel) + "\norientation: " + str(
                self.theta) + "\nangular vel: " + str(self.thetaVel)
