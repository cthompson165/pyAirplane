class Force:

    def __init__(self, name, position, vector):
        self.name = name
        self.position = position
        self.vector = vector

    def local_to_global(self, body_position, body_orientation):
        force_position = self.position.rotate(body_orientation).add(body_position)
        force_vector = self.vector.rotate(body_orientation)
        return Force(self.name, force_position, force_vector)

    def endpoint(self):
        return self.position.add(self.vector)

    def __str__(self):
        return self.name + ": " + str(self.vector) + " at " + str(self.position)
