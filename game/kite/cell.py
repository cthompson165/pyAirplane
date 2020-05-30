from aerodynamics.surface import Surface
from aerodynamics.lift_curves.flat_plate_empirical_lift import FlatPlateEmpiricalLift
from aerodynamics.drag_curves.flat_plate_drag import FlatPlateDrag
from util.angle import Angle
import math


class Cell(Surface):
    def __init__(self, name, position, length, width):
        span = self.calculate_span(width)
        area = self.calculate_area(span, length)
        aspect_ratio = self.calculate_aspect_ratio(span, area)

        # TODO - switch to empirical
        lift_curve = FlatPlateEmpiricalLift(aspect_ratio)
        drag_curve = FlatPlateDrag(aspect_ratio)

        Surface.__init__(
            self, name, position, length, Angle(0),
            area, lift_curve, drag_curve)

    def calculate_span(self, width):
        return 2 * width * math.cos(45)

    def calculate_area(self, span, length):
        area = length * span
        return 2 * area

    def calculate_aspect_ratio(self, span, area):
        return span**2 / area
