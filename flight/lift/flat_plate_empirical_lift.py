from flight.lift.empirical_lift import EmpiricalLift
from physics.vector_2d import Vector2D
from physics.angle import Angle


class FlatPlateEmpiricalLift(EmpiricalLift):
    ''' Approximated from curve in NASA paper:
    http://www.aerospaceweb.org/question/airfoils/q0150b.shtml '''

    def __init__(self, aspect_ratio):
        ''' Use 0 to ignor aspect_ratio '''

        if aspect_ratio <= 0:
            self._downwash_multiplier = 1
        else:
            self._downwash_multiplier = aspect_ratio / (2 + aspect_ratio)
            self._downwash_multiplier *= 2  # TODO...

        EmpiricalLift.__init__(self)

    def stall_angle(self):
        return Angle(13)

    def get_points(self):

        points = []
        points.append(self._adjust_for_ar(0, 0))
        points.append(self._adjust_for_ar(10, 1))
        points.append(self._adjust_for_ar(13, 1.08))
        points.append(self._adjust_for_ar(16, .6))
        points.append(self._adjust_for_ar(20, .6))
        points.append(self._adjust_for_ar(45, 1.05))
        points.append(self._adjust_for_ar(90, 0))

        return points

    def _adjust_for_ar(self, x, y):
        # TODO - this probably isn't legit...
        return Vector2D(x, self._downwash_multiplier * y)
