from simple_plane import SimplePlane
from util.vector_2d import Vector2D


class Bomber(SimplePlane):
    def __init__(self, pos, velocity):
        SimplePlane.__init__(self, pos, velocity)

    def get_force_vectors(self, mass, velocity):
        vectors = []

        ''' TODO: Add force vectors '''

        return vectors
