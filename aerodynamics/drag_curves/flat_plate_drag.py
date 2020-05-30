from aerodynamics.drag_curve import DragCurve
import math


class FlatPlateDrag(DragCurve):
    ''' from https://www.grc.nasa.gov/WWW/K-12/airplane/kitedrag.html '''
    def __init__(self, aspect_ratio):
        self._aspect_ratio = aspect_ratio

    def calculate_drag_coefficient(self, aoa, CL):
        cd0 = 1.28 * math.sin(aoa.radians())

        if self._aspect_ratio > 0:
            downwash = (CL**2) \
                / (.7 * math.pi * self._aspect_ratio)
            return cd0 + downwash
        else:
            return cd0
