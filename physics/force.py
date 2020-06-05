class Force:

    def __init__(self, name, pos, vector):
        self.name = name
        self.pos = pos
        self.vector = vector

    def local_to_global(self, body_position, body_orientation):
        force_position = self.pos.rotate(body_orientation).add(body_position)
        force_vector = self.vector.rotate(body_orientation)
        return Force(self.name, force_position, force_vector)

    def endpoint(self):
        return self.pos.add(self.vector)

    def __str__(self):
        return self.name + ": " + str(self.vector) + " at " + str(self.pos)
