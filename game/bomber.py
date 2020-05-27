from simple_plane import SimplePlane
from util.vector_2d import Vector2D


class Bomber(SimplePlane):
    def __init__(self, pos, velocity):
        SimplePlane.__init__(self, pos, velocity)
        self.iteration = 0

    def get_force_vectors(self, mass, velocity):
        vectors = []

        if self.iteration == 1:
            vectors.append(Vector2D(0, 1000))

        self.iteration = self.iteration + 1
        return vectors
