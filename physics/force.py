class Force:

    LIFT = 1
    DRAG = 2
    THRUST = 3
    GRAVITY = 4
    OTHER = 5

    def __init__(self, name, source, position, vector):
        self.name = name
        self.position = position
        self.vector = vector
        self.source = source

    def local_to_global(self, body_position, body_orientation):
        force_position = self.position.rotate(
            body_orientation).add(body_position)
        force_vector = self.vector.rotate(body_orientation)
        return Force(self.name, self.source, force_position, force_vector)

    def endpoint(self, scaling_factor=1):
        return self.position.add(self.vector.scale(scaling_factor))

    def __str__(self):
        return self.name + ": " + str(self.vector) \
            + " at " + str(self.position)
