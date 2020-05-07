from aerodynamics.surface import Surface
from aerodynamics.lift_curves.linear_lift import LinearLift
from aerodynamics.lift_curves.lifting_line_lift import LiftingLineLift
from aerodynamics.drag_curves.lifting_line_drag import LiftingLineDrag

class ThinAirfoil(Surface):

    def __init__(self, name, relative_pos, relative_degrees, area, aspect_ratio, CLa, CL0, CD0, efficiency_factor):
        Surface.__init__(self, name, relative_pos, relative_degrees, area)
        
        if CLa == 0:
            self.lift_curve = LiftingLineLift(aspect_ratio)
        else:
            self.lift_curve = LinearLift(aspect_ratio, CL0, CLa)

        self.drag_curve = LiftingLineDrag(aspect_ratio, CD0, efficiency_factor)
            
    def calculate_lift_coefficient(self, airplaneAngle, velocity):
        aoa = self.AoA(airplaneAngle, velocity)
        fc = self.lift_curve.calculate_lift_coefficient(aoa)
        return fc

    def calculate_drag_coefficient(self, airplaneAngle, velocity): 
        aoa = self.AoA(airplaneAngle, velocity)
        CL = self.lift_curve.calculate_lift_coefficient(aoa)
        return self.drag_curve.calculate_drag_coefficient(CL)


