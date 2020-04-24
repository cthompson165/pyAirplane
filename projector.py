from vector2d import Vector2D


class Projector:

    def __init__(self, screen_size, meters_per_pixel):
        self._screen_size = screen_size  # pixels
        self._meters_per_pixel = meters_per_pixel
        self._centering_offset = screen_size.scale(.5)  # pixels
        self._origin_offset = Vector2D(0, 0)  # pixels

    def project(self, real_pos):

        screen_pos = self.map_to_pixels(real_pos)

        # translate to origin
        screen_pos = screen_pos.subtract(self._origin_offset)
        return screen_pos

    def map_to_pixels(self, real_pos):
        # get pixels
        screen_pos = real_pos.scale(1.0 / self._meters_per_pixel)

        # flip y
        screen_pos = Vector2D(screen_pos.x,
                              self._screen_size.y - screen_pos.y)
        return screen_pos

    def center(self, real_pos):
        # TODO - options for whether or not to do this
        # keep centered
        projected = self.map_to_pixels(real_pos)
        self._origin_offset = projected.subtract(self._centering_offset)