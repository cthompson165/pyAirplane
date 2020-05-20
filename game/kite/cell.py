from aerodynamics.surface import Surface
from aerodynamics.lift_curves.lifting_line_lift import LiftingLineLift
from aerodynamics.drag_curves.lifting_line_drag import LiftingLineDrag
from util.angle import Angle
from util.vector_2d import Vector2D
import math


class Cell(Surface):
    def __init__(self, name, position, length, width):
        span = self.calculate_span(width)
        area = self.calculate_area(span, length)
        aspect_ratio = self.calculate_aspect_ratio(span, area)

        lift_curve = LiftingLineLift(aspect_ratio)
        drag_curve = LiftingLineDrag(aspect_ratio)

        aerodynamic_center = Vector2D(position.x - (length / 4.0), position.y)

        Surface.__init__(
            self, name, aerodynamic_center, Angle(0),
            area, lift_curve, drag_curve)

    def calculate_span(self, width):
        return 2 * width * math.cos(45)

    def calculate_area(self, span, length):
        area = length * span
        return 2 * area

    def calculate_aspect_ratio(self, span, area):
        return span**2 / area
