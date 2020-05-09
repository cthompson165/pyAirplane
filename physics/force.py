import enum


class Force:

    def __init__(self, source, name, pos, vector):
        self.name = name
        self.pos = pos
        self.vector = vector
        self.source = source

    class Source(enum.Enum):
        lift = 1
        drag = 2
        thrust = 3
        gravity = 4
        other = 5
