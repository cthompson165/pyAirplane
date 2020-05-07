import math
from aerodynamics.surface import Surface

class ThinAirfoil(Surface):

    def __init__(self, name, relative_pos, relative_degrees, area, aspect_ratio, CLa, CL0, CD0, efficiency_factor):
        Surface.__init__(self, name, relative_pos, relative_degrees, area)
        self.CLa = CLa
        self.CL0 = CL0
        self.CD0 = CD0
        self.aspect_ratio = aspect_ratio
        self.efficiency_factor = efficiency_factor

        # TODO - ever want CLa = 0?
        if self.CLa == 0:
            self.CLa = self.calculate_CLa_lifting_line(aspect_ratio)

    def calculate_CLa_lifting_line(self, aspect_ratio):
        return 2 * math.pi * (aspect_ratio / (2 + aspect_ratio))
            
    def calculate_lift_coefficient(self, airplaneAngle, velocity):
        aoa = self.AoA(airplaneAngle, velocity)

        # thin airfoil
        # CL = CLa * AoA + CL0
        CL = self.CLa * aoa.relativeRadians() + self.CL0
        return CL

    def calculate_drag_coefficient(self, airplaneAngle, velocity): 
        CL = self.calculate_lift_coefficient(airplaneAngle, velocity)
        
        induced_drag_coefficient = CL**2 / (math.pi * self.aspect_ratio)

        CD =  self.CD0 + induced_drag_coefficient / self.efficiency_factor
        
        return CD


