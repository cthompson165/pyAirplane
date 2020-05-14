from util.vector_2d import Vector2D


class Projector:

    def __init__(self, screen_size, meters_per_pixel):
        self._screen_size = screen_size  # pixels
        self._meters_per_pixel = meters_per_pixel
        self._centering_offset = screen_size.scale(.5)  # pixels
        self._origin_offset = Vector2D(0, 0)  # pixels

        self._pixels_per_meter = 1.0 / meters_per_pixel

    def project(self, real_pos):

        screen_pos = self._map_to_pixels(real_pos)

        # translate to origin
        screen_pos = screen_pos.subtract(self._origin_offset)
        return screen_pos

    def _map_to_pixels(self, real_pos):
        ''' get pixel position from world position '''
        screen_pos = real_pos.scale(self._pixels_per_meter)

        # flip y
        screen_pos = Vector2D(screen_pos.x,
                              self._screen_size.y - screen_pos.y)
        return screen_pos

    def center(self, real_pos):
        # TODO - options for whether or not to do this
        # keep centered
        projected = self._map_to_pixels(real_pos)
        self._origin_offset = projected.subtract(self._centering_offset)

    def center_x(self, real_pos):
        # TODO - options for whether or not to do this
        # keep centered
        projected = self._map_to_pixels(real_pos)
        self._origin_offset = Vector2D(
            projected.x - self._centering_offset.x, self._origin_offset.y)

    def get_pixels(self, meters):
        return meters * self._pixels_per_meter
