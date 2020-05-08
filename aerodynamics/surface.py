class Surface:
    ''' A plane has multiple services that generate lift
    and drag forces'''

    air_density = 0.30267

    def __init__(self, name, relative_pos,
                 relative_degrees, area, lift_curve, drag_curve):

        self.name = name
        self.relative_pos = relative_pos  # relative to CG
        self.relative_degrees = relative_degrees
        self.area = area

        self.lift_curve = lift_curve
        self.drag_curve = drag_curve

        self.distance_to_cg = relative_pos.magnitude()

    def aoa(self, airplane_angle, velocity):
        absolute_angle = airplane_angle.plus_constant(self.relative_degrees)

        velAngle = velocity.angle()
        return absolute_angle.minus(velAngle)

    def calculate_lift(self, airplane_angle, velocity):

        # equation from
        # http://www.aerospaceweb.org/question/aerodynamics/q0252.shtml
        aoa = self.aoa(airplane_angle, velocity)
        CL = self.lift_curve.calculate_lift_coefficient(aoa)

        vel_mag = velocity.magnitude()
        lift = (Surface.air_density * vel_mag**2 * self.area * CL) / 2

        return lift

    def calculate_drag(self, airplane_angle, velocity):

        aoa = self.aoa(airplane_angle, velocity)
        CL = self.lift_curve.calculate_lift_coefficient(aoa)

        # equation from
        # https://wright.nasa.gov/airplane/drageq.html
        CD = self.drag_curve.calculate_drag_coefficient(CL)

        vel_mag = velocity.magnitude()
        drag = CD * self.area * (Surface.air_density * vel_mag**2) / 2

        return drag
