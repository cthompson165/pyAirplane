from util.vector_2d import Vector2D
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

    def get_position(self):
        ''' position relative to knot angle with kite horizontal and
        knot angle at the back (negative x) '''
        return Vector2D(self._x, self._y)
