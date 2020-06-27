from flight.lift.empirical import Empirical
import physics
import math


class PlateEmpirical(Empirical):
    ''' Approximated from curve in NASA paper:
    http://www.aerospaceweb.org/question/airfoils/q0150b.shtml '''

    def __init__(self, aspect_ratio):
        ''' Use 0 to ignore aspect_ratio '''

        if aspect_ratio <= 0:
            self._PI_AR = 1
        else:
            self._PI_AR = math.pi * aspect_ratio

        Empirical.__init__(self)

    def stall_angle(self):
        return physics.Angle(13)

    def get_points(self):

        points = []
        points.append(physics.Vector2D(-180, 0))

        # trailing edge is leading with a negative aoa
        points.append(physics.Vector2D(-170, -self._get_cl(1)))
        points.append(physics.Vector2D(-167, -self._get_cl(1.08)))
        points.append(physics.Vector2D(-164, -self._get_cl(.6)))
        points.append(physics.Vector2D(-160, -self._get_cl(.6)))
        points.append(physics.Vector2D(-135, -self._get_cl(1.05)))

        points.append(physics.Vector2D(-90, 0))

        points.append(physics.Vector2D(-45, -self._get_cl(1.05)))
        points.append(physics.Vector2D(-20, -self._get_cl(.6)))
        points.append(physics.Vector2D(-16, -self._get_cl(.6)))
        points.append(physics.Vector2D(-13, -self._get_cl(1.08)))
        points.append(physics.Vector2D(-10, -self._get_cl(1)))

        points.append(physics.Vector2D(0, 0))
        points.append(physics.Vector2D(10, self._get_cl(1)))
        points.append(physics.Vector2D(13, self._get_cl(1.08)))
        points.append(physics.Vector2D(16, self._get_cl(.6)))
        points.append(physics.Vector2D(20, self._get_cl(.6)))
        points.append(physics.Vector2D(45, self._get_cl(1.05)))
        points.append(physics.Vector2D(90, self._get_cl(0)))

        # trailing edge is leading with a positive aoa
        points.append(physics.Vector2D(135, self._get_cl(1.05)))
        points.append(physics.Vector2D(160, self._get_cl(.6)))
        points.append(physics.Vector2D(164, self._get_cl(.6)))
        points.append(physics.Vector2D(167, self._get_cl(1.08)))
        points.append(physics.Vector2D(170, self._get_cl(1)))

        points.append(physics.Vector2D(180, 0))

        return points

    def _get_cl(self, cL0):
        # adapted from https://www.grc.nasa.gov/WWW/K-12/airplane/kitelift.html
        return cL0 / (1 + (cL0 / self._PI_AR))
