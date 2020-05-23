from aerodynamics.lift_curves.empirical_lift import EmpiricalLift
from util.vector_2d import Vector2D


class Naca63006EmpiricalLift(EmpiricalLift):
    ''' Approximated from curve in NASA paper:
    https://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/20140000500.pdf
    First 10 degrees adjusted matches lifting line (2*pi*aoa) '''

    def __init__(self, aspect_ratio):
        ''' Use 0 to ignor aspect_ratio '''

        if aspect_ratio <= 0:
            self._downwash_multiplier = 1
        else:
            self._downwash_multiplier = aspect_ratio / (2 + aspect_ratio)

        EmpiricalLift.__init__(self)

    def get_points(self):

        points = []
        points.append(self._adjust_for_ar(0, 0))
        points.append(self._adjust_for_ar(10, 1.0966))
        points.append(self._adjust_for_ar(13, 1.0966))
        points.append(self._adjust_for_ar(30, 1.15))
        points.append(self._adjust_for_ar(40, 1.1))
        points.append(self._adjust_for_ar(50, 1.17))
        points.append(self._adjust_for_ar(90, 0))

        return points

    def _adjust_for_ar(self, x, y):
        # TODO - this probably isn't legit...
        return Vector2D(x, self._downwash_multiplier * y)
