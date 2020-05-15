import enum


class Force:

    def __init__(self, source, name, pos, vector):
        self.name = name
        self.pos = pos
        self.vector = vector
        self.source = source

    def rotate(self, angle):
        return Force(self.source, self.name, self.pos.rotate(angle),
                     self.vector.rotate(angle))

    def __str__(self):
        return self.name + ": " + str(self.vector) + " at " + str(self.pos)

    class Source(enum.Enum):
        lift = 1
        drag = 2
        thrust = 3
        gravity = 4
        other = 5
