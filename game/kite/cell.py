from aerodynamics.surface import Surface
from aerodynamics.lift_curves.naca_63006_empirical \
    import Naca63006EmpiricalLift
from aerodynamics.drag_curves.flat_plate_drag import FlatPlateDrag
from util.angle import Angle
from util.vector_2d import Vector2D
import math


class Cell(Surface):
    def __init__(self, name, position, length, width):
        span = self.calculate_span(width)
        area = self.calculate_area(span, length)
        aspect_ratio = self.calculate_aspect_ratio(span, area)

        lift_curve = Naca63006EmpiricalLift()
        drag_curve = FlatPlateDrag(aspect_ratio)

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
