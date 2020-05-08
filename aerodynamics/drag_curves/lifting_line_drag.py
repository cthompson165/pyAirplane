import math
from aerodynamics.drag_curve import DragCurve


class LiftingLineDrag(DragCurve):
    ''' Implements drag curve based on lifting line theory '''

    def __init__(self, aspect_ratio, cd_min=0.025, efficiency_factor=0.75):

        self.aspect_ratio = aspect_ratio
        self.cd_min = cd_min
        self.efficiency_factor = efficiency_factor

    def calculate_drag_coefficient(self, coefficient_lift):
        ''' calculate drag coefficient '''
        induced_drag_coefficient = coefficient_lift**2 \
            / (math.pi * self.aspect_ratio)
        return self.cd_min \
            + induced_drag_coefficient \
            / self.efficiency_factor
