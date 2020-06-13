from physics.vector_2d import Vector2D
import math


class Bridle:
    def __init__(self, bridle_length, knot_length, kite_length):
        ''' bridle_length is total length of bridle string.
        knot_length is from bottom (back) of kite to the knot
        '''

        cos_bridle_angle = (knot_length**2 + kite_length**2
                            - (bridle_length - knot_length)**2) \
            / (2 * knot_length * kite_length)

        bridle_angle = math.acos(cos_bridle_angle)

        self._x = knot_length * math.cos(bridle_angle)
        self._y = -knot_length * math.sin(bridle_angle)

        self.initial_pos = Vector2D(0, 0)

    def get_position(self):
        ''' position relative to bottom attachment point of the kite
        with kite horizontal '''
        return Vector2D(self._x, self._y)
