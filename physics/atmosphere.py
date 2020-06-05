from util.vector_2d import Vector2D


class Atmosphere:
    def __init__(self):
        self.wind_speed = Vector2D(0, 0)

        # the  density is of air at 12,192 meters
        # is approximately 0.30267 kg/m3
        self._air_density = 0.30267

    def get_air_density(self, altitude):
        return self._air_density  # TODO
