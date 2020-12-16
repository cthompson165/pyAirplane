from physics.vector_2d import Vector2D


class Projector:

    def __init__(self, screen_size, meters_per_pixel=1.0):
        self._screen_size = screen_size  # pixels
        self._meters_per_pixel = meters_per_pixel
        self._centering_offset = screen_size.scale(.5)  # pixels
        self._origin_offset = Vector2D(0, 0)  # pixels

        self.set_meters_per_pixel(meters_per_pixel)
        self._current_real_pos = Vector2D(0, 0)

    def set_meters_per_pixel(self, meters_per_pixel):
        self._meters_per_pixel = meters_per_pixel
        self._pixels_per_meter = 1.0 / meters_per_pixel
        screen_meters = self._screen_size.scale(meters_per_pixel)
        self._half_screen_meters = screen_meters.scale(1/2)

    def set_resolution(self, pixels, meters):
        self.set_meters_per_pixel(meters / pixels)

    def project(self, real_pos):

        screen_pos = self._map_to_pixels(real_pos)

        # translate to origin
        screen_pos = screen_pos.subtract(self._origin_offset)
        return (int(screen_pos.x), int(screen_pos.y))

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
        self._current_real_pos = real_pos
        projected = self._map_to_pixels(real_pos)
        self._origin_offset = projected.subtract(self._centering_offset)

    def center_x(self, real_pos):
        # TODO - options for whether or not to do this
        # keep centered
        self._current_real_pos = real_pos
        projected = self._map_to_pixels(real_pos)
        self._origin_offset = Vector2D(
            projected.x - self._centering_offset.x, self._origin_offset.y)

    def get_pixels(self, meters):
        return int(meters * self._pixels_per_meter)

    def get_top_left(self):
        return Vector2D(self._current_real_pos.x - self._half_screen_meters.x,
                        self._current_real_pos.y + self._half_screen_meters.y)

    def get_bottom_right(self):
        return Vector2D(self._current_real_pos.x + self._half_screen_meters.x,
                        self._current_real_pos.y - self._half_screen_meters.y)

    def is_on_screen(self, screen_pos):
        return not (screen_pos[0] < 0 or
                    screen_pos[1] < 0 or
                    screen_pos[0] > self._screen_size.x or
                    screen_pos[1] > self._screen_size.y)
