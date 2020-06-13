from flight.surface import Surface
from physics.angle import Angle
import math
import flight.drag as drag
import flight.lift as lift


class Cell(Surface):
    def __init__(self, name, position, length, width, atmosphere):
        span = self.calculate_span(width)
        area = self.calculate_area(span, length)
        aspect_ratio = self.calculate_aspect_ratio(span, area)

        lift_curve = lift.PlateEmpirical(aspect_ratio)
        drag_curve = drag.FlatPlate(aspect_ratio)

        Surface.__init__(
            self, name, position, length, Angle(0),
            area, lift_curve, drag_curve, atmosphere)

    def calculate_span(self, width):
        return 2 * width * math.cos(45)

    def calculate_area(self, span, length):
        area = length * span
        return 2 * area

    def calculate_aspect_ratio(self, span, area):
        return span**2 / area
