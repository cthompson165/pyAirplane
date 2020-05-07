import math
from aerodynamics.drag_curve import DragCurve

class LiftingLineDrag(DragCurve):
    def __init__(self, aspect_ratio, CD_min=0.025, efficiency_factor=0.75):

        self.aspect_ratio = aspect_ratio
        self.CD_min = CD_min
        self.efficiency_factor = efficiency_factor

    def calculate_drag_coefficient(self, CL):

        induced_drag_coefficient = CL**2 / (math.pi * self.aspect_ratio)

        return self.CD_min + induced_drag_coefficient / self.efficiency_factor 