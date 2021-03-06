from flight.lift_curve import LiftCurve


class Empirical(LiftCurve):
    ''' Define points on a lift curve
        Assumes symmetrical lift for huge angles
        of attack (flying backward...)
    '''
    def __init__(self):
        # TODO - cache the diff unit vectors
        # between all the points
        self._points = self.get_points()

    def get_points(self):
        ''' points sorted by aoa in degrees '''
        raise NotImplementedError

    def calculate_lift_coefficient(self, aoa):

        aoa_degrees = aoa.relative_degrees()
        previous_point = self._points[0]
        for i in range(1, len(self._points)):
            next_point = self._points[i]
            if aoa_degrees <= next_point.x:
                return self._get_cl_between_points(
                    aoa_degrees, previous_point, next_point)
                break
            previous_point = next_point

        raise EOFError()

    def _get_cl_between_points(self, aoa_degrees, point1, point2):
        diff_vector = point2.subtract(point1)
        percent = (aoa_degrees - point1.x) / (point2.x - point1.x)
        cl = point1.add(diff_vector.scale(percent)).y
        return cl
